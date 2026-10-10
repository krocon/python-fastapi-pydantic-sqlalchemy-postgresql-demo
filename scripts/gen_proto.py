"""uv run python -m scripts.gen_proto – regenerate app/proto/users_pb2.py (+ .pyi) from users.proto."""

import sys

from grpc_tools import protoc

ARGS = ["protoc", "-Iapp/proto", "--python_out=app/proto", "--pyi_out=app/proto", "app/proto/users.proto"]
sys.exit(protoc.main(ARGS))
