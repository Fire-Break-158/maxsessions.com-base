##
## Library Imports
##
# Standard library imports
import functools
import inspect
import os

# Third-party imports
from flask import (
    current_app,
    session
)
import psycopg2.pool
import jwt



def check_permission(client_roles, required_permissions):
    return any(role in required_permissions for role in client_roles)



def get_oidc_user_info(oidc):
    if session['id_token']:
        id_token = session['id_token']
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        client_roles = decoded_token.get('resource_access', {}).get(os.environ.get("CLIENT_ID"), {}).get('roles', [])
        info = oidc.user_getinfo(['preferred_username', 'email','name'])
        info['client_roles'] = client_roles
        return (info)
    else:
        info = "False"
        return(info)
    


def with_postgres_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        def db_connect(config):
            db_connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=config['MAX_POOL_SIZE'],
                dbname=config['DBNAME'],
                user=config['DBUSER'],
                password=config['DBPASS'],
                host=config['DBHOST'], 
                port=config['DBPORT']
            )
            return(db_connection_pool)
        # Step 1: Get the function signature
        sig = inspect.signature(func)

        # Step 2: Bind provided arguments to the function's signature
        bound_args = sig.bind_partial(*args, **kwargs)
        bound_args.apply_defaults()

        # Step 3: Extract the positional arguments and parameters
        args = list(bound_args.args)  # The provided positional arguments
        kwargs = bound_args.kwargs  # The provided keyword arguments
        parameters = list(sig.parameters.values())  # The function's parameters

        # Step 4: Check if the number of provided positional arguments is one less than required
        # This checks if 'db' is missing
        if len(args) < len(parameters) and 'db' not in kwargs:
            # Step 5: Assume 'db' is missing, so acquire a connection
            conn = current_app.db_connection_pool.getconn()
            if conn is None:
                return "Failed to acquire PostgreSQL connection"
            try:
                # Find the correct position for 'db' in the parameters
                for i, param in enumerate(parameters):
                    if param.name == 'db':
                        args.insert(i, conn)
                        break

                # Step 6: Call the original function with the updated arguments
                result = func(*args, **kwargs)
            except psycopg2.OperationalError as e:
                if str(e) == "server closed the connection unexpectedly":
                    # Reestablish the connection pool and connection
                    current_app.db_connection_pool = db_connect(current_app.config)
                    conn = current_app.db_connection_pool.getconn()
                    for i, param in enumerate(parameters):
                        if param.name == 'db':
                            args.insert(i, conn)
                            break
                    result = func(*args, **kwargs)
                else:
                    # Reraise the exception if it's not the expected error
                    raise
            finally:
                # Release the connection back to the pool
                current_app.db_connection_pool.putconn(conn)
        else:
            # 'db' is provided, call the function directly
            result = func(*args, **kwargs)
        return result
    return wrapper      