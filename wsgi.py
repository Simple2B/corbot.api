#!/user/bin/env python

from app import create_app, db, forms

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, forms=forms)


if __name__ == "__main__":
    app.run()
