import sys
import os
import importlib.util

backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'back-end')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Circular import 방지를 위해 back-end/app.py를 동적으로 로드합니다.
spec = importlib.util.spec_from_file_location("backend_app", os.path.join(backend_dir, "app.py"))
backend_module = importlib.util.module_from_spec(spec)
sys.modules["backend_app"] = backend_module
spec.loader.exec_module(backend_module)

# Cloudtype(Gunicorn)이 이 변수를 찾을 수 있도록 노출합니다.
app = backend_module.app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
