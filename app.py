from app import create_app

if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)

    # app.run(debug=os.environ.get('FLASK_ENV') == 'development')
