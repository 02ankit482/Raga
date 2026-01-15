import os
import argparse

from app import create_app


def main():
    parser = argparse.ArgumentParser(description="Run the RAG Flask app")

    parser.add_argument(
        "--host",
        default=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        help="Host to bind to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("FLASK_RUN_PORT", 5000)),
        help="Port to bind to",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )
    parser.add_argument(
        "--no-debug",
        dest="debug",
        action="store_false",
        help="Disable debug mode",
    )

    parser.set_defaults(debug=None)
    args = parser.parse_args()

    app = create_app()

    # Resolve debug mode
    if args.debug is None:
        debug = bool(app.config.get("DEBUG", False))
    else:
        debug = args.debug

    print(f"🚀 Starting app on http://{args.host}:{args.port} (debug={debug})")
    app.run(host=args.host, port=args.port, debug=debug)


if __name__ == "__main__":
    main()
