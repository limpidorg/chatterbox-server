from Global import API, app
import views.session
import views.chat

if __name__ == "__main__":
    API.run(app, port=3002, host="0.0.0.0")
