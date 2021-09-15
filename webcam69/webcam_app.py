from app import get_app, init_db
import views_manager


async def webcam_app():
    app = get_app()
    manager = views_manager.ViewsManager(app=app)
    manager.register_routes()
    await init_db()
    return app
