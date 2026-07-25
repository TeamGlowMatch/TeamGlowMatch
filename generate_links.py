import pandas as pd

df_products = pd.read_csv("Products.csv")
df_ingredients = pd.read_csv("Ingredients.csv")

df_ingredients["Ingredient_Name_Clean"] = (
    df_ingredients["Ingredient_Name"].astype(str).str.strip().str.lower()
)

ing_map = dict(
    zip(
        df_ingredients["Ingredient_Name_Clean"],
        df_ingredients["Ingredient_Id"],
    )
)

links = []
link_counter = 1

for _, prod_row in df_products.iterrows():
    p_id = prod_row["Product_Id"]
    raw_ing_text = str(prod_row["Ingredients"])

    product_ings = {
        x.strip().lower() for x in raw_ing_text.split(",") if len(x.strip()) > 0
    }

    for ing_name_clean, ing_id in ing_map.items():
        if ing_name_clean in product_ings:
            links.append(
                {
                    "Link_Id": f"LINK_{link_counter:05d}",
                    "Product_Id": p_id,
                    "Ingredient_Id": ing_id,
                }
            )
            link_counter += 1

df_links = pd.DataFrame(links)
df_links = df_links.drop_duplicates(subset=["Product_Id", "Ingredient_Id"])
df_links.to_csv("Product_Ingredients.csv", index=False, encoding="utf-8-sig")