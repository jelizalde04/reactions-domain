import os
import sys
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def test_env_file_exists():
    env_path = os.path.join(BASE_DIR, ".env")
    assert os.path.exists(env_path), ".env file does not exist"

def test_required_env_variables():
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "PET_DB_NAME","POST_DB_NAME", "REACTIONS_DB_NAME", "DB_PORT", "JWT_SECRET"]
    missing = [var for var in required_vars if not os.getenv(var)]
    assert not missing, f"Missing required environment variables: {missing}"

def test_main_app_importable():
    app_path = os.path.join(BASE_DIR, "app.py")
    spec = importlib.util.spec_from_file_location("app", app_path)
    assert spec is not None, "app.py cannot be found"
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        assert False, f"app.py could not be imported: {e}" 