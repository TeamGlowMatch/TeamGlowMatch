
CREATE TABLE Brands (
    Brand_ID VARCHAR(50) NOT NULL PRIMARY KEY,
    Brand_Name VARCHAR(255) NOT NULL,
    Country VARCHAR(100),
    Popularity_Score INT
);

CREATE TABLE Ingredients (
    Ingredient_Id NVARCHAR(50) NOT NULL PRIMARY KEY,
    Ingredient_Name NVARCHAR(255) NOT NULL,
    Main_Role NVARCHAR(255),
    Hydration_Level NVARCHAR(50),
    Is_Active_Ingredient NVARCHAR(50)
);


CREATE TABLE Products (
    Product_Id VARCHAR(50) NOT NULL PRIMARY KEY,
    Brand VARCHAR(100),
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(100),
    Country VARCHAR(100),
    Ingredients VARCHAR(MAX),
    AfterUse VARCHAR(MAX),
);


CREATE TABLE Product_Ingredients (
    Link_Id VARCHAR(50) NOT NULL PRIMARY KEY,
    Product_Id VARCHAR(50),
    Ingredient_Id VARCHAR(50),
    FOREIGN KEY (Product_Id) REFERENCES Products(Product_Id),
    FOREIGN KEY (Ingredient_Id) REFERENCES Ingredients(Ingredient_Id)
);

CREATE TABLE Clinics (
    Clinic_ID NVARCHAR(50) NOT NULL PRIMARY KEY,
    Clinic_Name NVARCHAR(255) NOT NULL,
    City NVARCHAR(100) NOT NULL
);

