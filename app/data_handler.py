import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1. Database Configuration
# Replace with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://admin:secret@localhost:5432/mandir_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Financial Year ID
# This assumes you have the 'financial_years' table and know the ID
# for the current financial year. You might get this from your database.
FINANCIAL_YEAR_ID1 = 1
FINANCIAL_YEAR_ID2 = 2
FINANCIAL_YEAR_ID3 = 3
FINANCIAL_YEAR_ID4 = 4
FINANCIAL_YEAR_ID5 = 5


def import_from_excel(file_path, sheet_name, TOLA_ID):
    # Read the Excel sheet into a pandas DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
    print("Excel data loaded successfully.")

    # Start a database session
    db = SessionLocal()
    try:
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            contributor_name = row['Name']
            base_amount = row['Old Donation Amount']
            T2022_amount = row['Donation Amount -2022']
            print(base_amount)
            # 3. Insert into 'contributors' table
            # SQL query to insert a new contributor and return their ID
            contributor_sql = text("""
                INSERT INTO contributors (name, created_at, updated_at,tola_id)
                VALUES (:name, NOW(), NOW(), :tola_id)
                RETURNING id;
            """)

            contributor_sql = text("""
                INSERT INTO contributors (name, created_at, updated_at,tola_id)
                VALUES (:name, NOW(), NOW(), :tola_id)
                RETURNING id;
            """)

            # Execute the query and get the returned ID
            result = db.execute(
                contributor_sql, {"name": contributor_name, "tola_id": TOLA_ID})
            contributor_id = result.scalar()  # Get the single ID value
            print(
                f"Inserted contributor '{contributor_name}' with ID: {contributor_id}")

            # 4. Insert into 'pledges' table
            # SQL query to insert the pledge using the new contributor_id
            pledge_sql = text("""
                INSERT INTO pledges (contributor_id, financial_year_id, amount, created_at)
                VALUES (:contributor_id, :financial_year_id, :amount, NOW());
            """)

            db.execute(pledge_sql, {
                "contributor_id": contributor_id,
                "financial_year_id": FINANCIAL_YEAR_ID1,
                "amount": base_amount
            })
            pledge_sql1 = text("""
                INSERT INTO pledges (contributor_id, financial_year_id, amount, created_at)
                VALUES (:contributor_id, :financial_year_id, :amount, NOW());
            """)

            db.execute(pledge_sql1, {
                "contributor_id": contributor_id,
                "financial_year_id": FINANCIAL_YEAR_ID2,
                "amount": T2022_amount
            })
            pledge_sql2 = text("""
                INSERT INTO pledges (contributor_id, financial_year_id, amount, created_at)
                VALUES (:contributor_id, :financial_year_id, :amount, NOW());
            """)

            db.execute(pledge_sql2, {
                "contributor_id": contributor_id,
                "financial_year_id": FINANCIAL_YEAR_ID3,
                "amount": T2022_amount
            })
            pledge_sql3 = text("""
                INSERT INTO pledges (contributor_id, financial_year_id, amount, created_at)
                VALUES (:contributor_id, :financial_year_id, :amount, NOW());
            """)

            db.execute(pledge_sql3, {
                "contributor_id": contributor_id,
                "financial_year_id": FINANCIAL_YEAR_ID4,
                "amount": T2022_amount
            })
            pledge_sql4 = text("""
                INSERT INTO pledges (contributor_id, financial_year_id, amount, created_at)
                VALUES (:contributor_id, :financial_year_id, :amount, NOW());
            """)

            db.execute(pledge_sql4, {
                "contributor_id": contributor_id,
                "financial_year_id": FINANCIAL_YEAR_ID5,
                "amount": T2022_amount
            })
            print(
                f"  --> Inserted pledge of {base_amount} for contributor ID {contributor_id}")

        # 5. Commit the changes
        db.commit()
        print("\nAll data imported and committed successfully!")

    except Exception as e:
        print(e)
        print(f"\nAn error occurred: {e}")
        db.rollback()  # Roll back all changes if any step fails
        print("Transaction rolled back.")

    finally:
        db.close()


# 6. Run the script
if __name__ == "__main__":
    excel_file = 'BhojPandaul_Jagdamba_Puja_Donation_List_2022.xlsx'
    sheets = ["1.DakshinwariTol", "2.Chaudhary Tol", "3.Malik Tol", "4.Purohit & Kayasth Tol",
              "5.Purwari Tol", "6.Puchwari Tol", "7.Karmahe Tol", "8.Goth Tol", "9. Chaupal Tol", "10.Kamti Tol"]
    tola_ids = [1, 5, 4, 6, 2, 7, 3, 8, 9, 10]
    for sheet, tola_id in zip(sheets, tola_ids):
        print(f"Running {sheet} and {tola_id}")
        sheet_name = sheet
        tola_id = tola_id
        import_from_excel(excel_file, sheet_name, tola_id)
