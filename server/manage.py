from app import create_app, db
from flask_migrate import Migrate
from app.models import Product, ProductionRuns, Ingredient, Recipe, RecipeIngredient

app = create_app("default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_processor():
    return dict(
        db=db,
        Product=Product,
        ProductionRuns=ProductionRuns,
        Ingredient=Ingredient,
        Recipe=Recipe,
        RecipeIngredient=RecipeIngredient
    )

if __name__ == "__main__":
    app.run(debug=True)