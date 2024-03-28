if __name__ == "__main__":
    from app import create_app, scrape_and_update
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False)
    scrape_and_update()