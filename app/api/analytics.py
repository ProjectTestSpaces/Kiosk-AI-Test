# from fastapi import APIRouter, HTTPException, Query
# from app.db import database
# from sqlalchemy import text
# from datetime import date


# router = APIRouter(prefix="/admin/analytics", tags=["Sales Analytics"])


# @router.get("/daily-sales", summary="Daily Sales Per Shop")
# async def get_daily_sales(date_filter: date = Query(..., description="Date in YYYY-MM-DD format")):
#     query = text("""
#         SELECT shop_id, SUM(total_amount) AS daily_total
#         FROM sales_transactions
#         WHERE transaction_date = :date
#         GROUP BY shop_id
#     """)
#     results = await database.fetch_all(query, {"date": date_filter})
#     return [{"shop_id": str(r["shop_id"]), "daily_total": float(r["daily_total"])} for r in results]

# @router.get("/all-sales", summary="All Sales")
# async def get_all_sales():
#     query = text("""
#         SELECT * FROM sales_transactions    
#     """)
#     results = await database.fetch_all(query)
#     return [dict(r) for r in results]  # convert result rows to dicts



# @router.get("/monthly-sales", summary="Total Sales for the Month")
# async def get_monthly_sales(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
#     query = text("""
#         SELECT DATE_TRUNC('month', transaction_date) AS month, SUM(total_amount) AS monthly_total
#         FROM sales_transactions
#         WHERE EXTRACT(MONTH FROM transaction_date) = :month
#         AND EXTRACT(YEAR FROM transaction_date) = :year
#         GROUP BY 1
#     """)
#     results = await database.fetch_all(query, {"month": month, "year": year})
#     if results:
#         return {"month": results[0]["month"], "monthly_total": float(results[0]["monthly_total"])}
#     return {"message": "No sales data found for the given month."}

from fastapi import APIRouter, HTTPException, Query
from app.db import database
from sqlalchemy import text
from datetime import date


router = APIRouter(prefix="/admin/analytics", tags=["Sales Analytics"])


# @router.get("/daily-sales", summary="Daily Sales Per Shop")
# async def get_daily_sales(date_filter: date = Query(..., description="Date in YYYY-MM-DD format")):
#     try:
#         # Method 1: Using values() method with text()
#         # query = text("""
#         #     SELECT shop_id, SUM(total_amount) AS daily_total
#         #     FROM sales_transactions
#         #     WHERE transaction_date = :date_param
#         #     GROUP BY shop_id
#         # """).values(date_param=date_filter)
        
#         # results = await database.fetch_all(query)
        
#         # Alternative Method 2: If Method 1 doesn't work, try this
#         query = text("""
#             SELECT shop_id, SUM(total_amount) AS daily_total
#             FROM sales_transactions
#             WHERE transaction_date = :date_param
#             GROUP BY shop_id
#         """)
#         results = await database.fetch_all(query, values={"date_param": date_filter})
        
#         return [{"shop_id": str(r["shop_id"]), "daily_total": float(r["daily_total"])} for r in results]
    
#     except Exception as e:
#         print(f"Database error in daily_sales: {e}")
#         raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# @router.get("/monthly-sales", summary="Total Sales for the Month")
# async def get_monthly_sales(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
#     try:
#         # Method 1: Using values() method with text()
#         # query = text("""
#         #     SELECT DATE_TRUNC('month', transaction_date) AS month, SUM(total_amount) AS monthly_total
#         #     FROM sales_transactions
#         #     WHERE EXTRACT(MONTH FROM transaction_date) = :month_param
#         #     AND EXTRACT(YEAR FROM transaction_date) = :year_param
#         #     GROUP BY DATE_TRUNC('month', transaction_date)
#         # """).values(month_param=month, year_param=year)
        
#         # results = await database.fetch_all(query)
        
#         # Alternative Method 2: If Method 1 doesn't work, try this
#         query = text("""
#             SELECT DATE_TRUNC('month', transaction_date) AS month, SUM(total_amount) AS monthly_total
#             FROM sales_transactions
#             WHERE EXTRACT(MONTH FROM transaction_date) = :month_param
#             AND EXTRACT(YEAR FROM transaction_date) = :year_param
#             GROUP BY DATE_TRUNC('month', transaction_date)
#         """)
#         results = await database.fetch_all(query, values={"month_param": month, "year_param": year})
        
#         if results:
#             return {"month": results[0]["month"], "monthly_total": float(results[0]["monthly_total"])}
#         return {"message": "No sales data found for the given month."}
    
#     except Exception as e:
#         print(f"Database error in monthly_sales: {e}")
#         raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Daily Sales
# GET http://127.0.0.1:8000/admin/analytics/daily-sales-alt?date_filter=2024-06-20 
@router.get("/daily-sales-alt", summary="Daily Sales Per Shop (Alternative)")
async def get_daily_sales_alt(date_filter: date = Query(..., description="Date in YYYY-MM-DD format")):
    try:
        # Convert date to string for SQL
        date_str = date_filter.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT shop_id, SUM(total_amount) AS daily_total
            FROM sales_transactions
            WHERE transaction_date = '{date_str}'
            GROUP BY shop_id
        """
        
        results = await database.fetch_all(query)
        return [{"shop_id": str(r["shop_id"]), "daily_total": float(r["daily_total"])} for r in results]
    
    except Exception as e:
        print(f"Database error in daily_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

# Monthly Sales
# GET http://127.0.0.1:8000/admin/analytics/monthly-sales-alt?month=6&year=2024
@router.get("/monthly-sales-alt", summary="Total Sales for the Month (Alternative)")
async def get_monthly_sales_alt(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
    try:
        query = f"""
            SELECT DATE_TRUNC('month', transaction_date) AS month, SUM(total_amount) AS monthly_total
            FROM sales_transactions
            WHERE EXTRACT(MONTH FROM transaction_date) = {month}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY DATE_TRUNC('month', transaction_date)
        """
        
        results = await database.fetch_all(query)
        
        if results:
            return {"month": results[0]["month"], "monthly_total": float(results[0]["monthly_total"])}
        return {"message": "No sales data found for the given month."}
    
    except Exception as e:
        print(f"Database error in monthly_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

# Weekly Sales
# GET http://127.0.0.1:8000/admin/analytics/weekly-sales-alt?start_date=2024-06-17&end_date=2024-06-23
@router.get("/weekly-sales-alt", summary="Total Sales for the Week (Alternative)")
async def get_weekly_sales_alt(
    start_date: date = Query(..., description="Start date of the week in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date of the week in YYYY-MM-DD format")
):
    try:
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                DATE_TRUNC('week', transaction_date) AS week_start,
                SUM(total_amount) AS weekly_total,
                COUNT(*) AS transaction_count
            FROM sales_transactions
            WHERE transaction_date >= '{start_str}' 
            AND transaction_date <= '{end_str}'
            GROUP BY DATE_TRUNC('week', transaction_date)
            ORDER BY week_start
        """
        
        results = await database.fetch_all(query)
        
        if results:
            return [
                {
                    "week_start": r["week_start"],
                    "weekly_total": float(r["weekly_total"]),
                    "transaction_count": r["transaction_count"]
                } for r in results
            ]
        return {"message": "No sales data found for the given week range."}
    
    except Exception as e:
        print(f"Database error in weekly_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Yearly Sales
# GET http://127.0.0.1:8000/admin/analytics/yearly-sales-alt?year=2024
@router.get("/yearly-sales-alt", summary="Total Sales for the Year (Alternative)")
async def get_yearly_sales_alt(year: int = Query(..., description="Year (e.g., 2024)")):
    try:
        query = f"""
            SELECT 
                EXTRACT(YEAR FROM transaction_date) AS year,
                SUM(total_amount) AS yearly_total,
                COUNT(*) AS transaction_count,
                COUNT(DISTINCT shop_id) AS active_shops
            FROM sales_transactions
            WHERE EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY EXTRACT(YEAR FROM transaction_date)
        """
        
        results = await database.fetch_all(query)
        
        if results:
            return {
                "year": int(results[0]["year"]),
                "yearly_total": float(results[0]["yearly_total"]),
                "transaction_count": results[0]["transaction_count"],
                "active_shops": results[0]["active_shops"]
            }
        return {"message": f"No sales data found for year {year}."}
    
    except Exception as e:
        print(f"Database error in yearly_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Quarterly Sales
# GET http://127.0.0.1:8000/admin/analytics/quarterly-sales-alt?quarter=2&year=2024
@router.get("/quarterly-sales-alt", summary="Total Sales for the Quarter (Alternative)")
async def get_quarterly_sales_alt(
    quarter: int = Query(..., ge=1, le=4, description="Quarter (1-4)"),
    year: int = Query(..., description="Year (e.g., 2024)")
):
    try:
        query = f"""
            SELECT 
                EXTRACT(QUARTER FROM transaction_date) AS quarter,
                EXTRACT(YEAR FROM transaction_date) AS year,
                SUM(total_amount) AS quarterly_total,
                COUNT(*) AS transaction_count,
                COUNT(DISTINCT shop_id) AS active_shops
            FROM sales_transactions
            WHERE EXTRACT(QUARTER FROM transaction_date) = {quarter}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY EXTRACT(QUARTER FROM transaction_date), EXTRACT(YEAR FROM transaction_date)
        """
        
        results = await database.fetch_all(query)
        
        if results:
            return {
                "quarter": int(results[0]["quarter"]),
                "year": int(results[0]["year"]),
                "quarterly_total": float(results[0]["quarterly_total"]),
                "transaction_count": results[0]["transaction_count"],
                "active_shops": results[0]["active_shops"]
            }
        return {"message": f"No sales data found for Q{quarter} {year}."}
    
    except Exception as e:
        print(f"Database error in quarterly_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Half-Yearly Sales
# First half (Jan-Jun)
# GET http://127.0.0.1:8000/admin/analytics/half-yearly-sales-alt?half=1&year=2024

# # Second half (Jul-Dec)
# GET http://127.0.0.1:8000/admin/analytics/half-yearly-sales-alt?half=2&year=2024

@router.get("/half-yearly-sales-alt", summary="Total Sales for Half Year (Alternative)")
async def get_half_yearly_sales_alt(
    half: int = Query(..., ge=1, le=2, description="Half year (1 for Jan-Jun, 2 for Jul-Dec)"),
    year: int = Query(..., description="Year (e.g., 2024)")
):
    try:
        # Determine month range based on half
        if half == 1:
            start_month, end_month = 1, 6
            period_name = "H1"
        else:
            start_month, end_month = 7, 12
            period_name = "H2"
        
        query = f"""
            SELECT 
                SUM(total_amount) AS half_yearly_total,
                COUNT(*) AS transaction_count,
                COUNT(DISTINCT shop_id) AS active_shops,
                MIN(transaction_date) AS period_start,
                MAX(transaction_date) AS period_end
            FROM sales_transactions
            WHERE EXTRACT(MONTH FROM transaction_date) >= {start_month}
            AND EXTRACT(MONTH FROM transaction_date) <= {end_month}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
        """
        
        results = await database.fetch_all(query)
        
        if results and results[0]["half_yearly_total"]:
            return {
                "half": half,
                "period": period_name,
                "year": year,
                "half_yearly_total": float(results[0]["half_yearly_total"]),
                "transaction_count": results[0]["transaction_count"],
                "active_shops": results[0]["active_shops"],
                "period_start": results[0]["period_start"],
                "period_end": results[0]["period_end"]
            }
        return {"message": f"No sales data found for {period_name} {year}."}
    
    except Exception as e:
        print(f"Database error in half_yearly_sales_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Bonus: Shop-wise Weekly Sales
# GET http://127.0.0.1:8000/admin/analytics/weekly-sales-by-shop-alt?start_date=2024-06-17&end_date=2024-06-23
@router.get("/weekly-sales-by-shop-alt", summary="Weekly Sales Per Shop (Alternative)")
async def get_weekly_sales_by_shop_alt(
    start_date: date = Query(..., description="Start date of the week in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date of the week in YYYY-MM-DD format")
):
    try:
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS weekly_total,
                COUNT(*) AS transaction_count,
                DATE_TRUNC('week', MIN(transaction_date)) AS week_start
            FROM sales_transactions
            WHERE transaction_date >= '{start_str}' 
            AND transaction_date <= '{end_str}'
            GROUP BY shop_id
            ORDER BY weekly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "shop_id": str(r["shop_id"]),
                "weekly_total": float(r["weekly_total"]),
                "transaction_count": r["transaction_count"],
                "week_start": r["week_start"]
            } for r in results
        ]
    
    except Exception as e:
        print(f"Database error in weekly_sales_by_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")

# Monthly Sales Per Shop
# GET http://127.0.0.1:8000/admin/analytics/monthly-sales-per-shop-alt?month=6&year=2024
@router.get("/monthly-sales-per-shop-alt", summary="Monthly Sales Per Shop (Alternative)")
async def get_monthly_sales_per_shop_alt(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
    try:
        query = f"""
            SELECT 
                shop_id, 
                SUM(total_amount) AS monthly_total,
                COUNT(*) AS transaction_count,
                DATE_TRUNC('month', MIN(transaction_date)) AS month
            FROM sales_transactions
            WHERE EXTRACT(MONTH FROM transaction_date) = {month}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY shop_id
            ORDER BY monthly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        if results:
            return [
                {
                    "shop_id": str(r["shop_id"]),
                    "monthly_total": float(r["monthly_total"]),
                    "transaction_count": r["transaction_count"],
                    "month": r["month"]
                } for r in results
            ]
        return {"message": "No sales data found for the given month."}
    
    except Exception as e:
        print(f"Database error in monthly_sales_per_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Weekly Sales Per Shop
# GET http://127.0.0.1:8000/admin/analytics/weekly-sales-per-shop-alt?start_date=2024-06-17&end_date=2024-06-23
@router.get("/weekly-sales-per-shop-alt", summary="Weekly Sales Per Shop (Alternative)")
async def get_weekly_sales_per_shop_alt(
    start_date: date = Query(..., description="Start date of the week in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date of the week in YYYY-MM-DD format")
):
    try:
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS weekly_total,
                COUNT(*) AS transaction_count,
                DATE_TRUNC('week', MIN(transaction_date)) AS week_start,
                DATE_TRUNC('week', MAX(transaction_date)) AS week_end
            FROM sales_transactions
            WHERE transaction_date >= '{start_str}' 
            AND transaction_date <= '{end_str}'
            GROUP BY shop_id
            ORDER BY weekly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "shop_id": str(r["shop_id"]),
                "weekly_total": float(r["weekly_total"]),
                "transaction_count": r["transaction_count"],
                "week_start": r["week_start"],
                "week_end": r["week_end"]
            } for r in results
        ]
    
    except Exception as e:
        print(f"Database error in weekly_sales_per_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Yearly Sales Per Shop
# GET http://127.0.0.1:8000/admin/analytics/yearly-sales-per-shop-alt?year=2024
@router.get("/yearly-sales-per-shop-alt", summary="Yearly Sales Per Shop (Alternative)")
async def get_yearly_sales_per_shop_alt(year: int = Query(..., description="Year (e.g., 2024)")):
    try:
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS yearly_total,
                COUNT(*) AS transaction_count,
                MIN(transaction_date) AS first_transaction,
                MAX(transaction_date) AS last_transaction,
                COUNT(DISTINCT DATE(transaction_date)) AS active_days
            FROM sales_transactions
            WHERE EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY shop_id
            ORDER BY yearly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "shop_id": str(r["shop_id"]),
                "yearly_total": float(r["yearly_total"]),
                "transaction_count": r["transaction_count"],
                "first_transaction": r["first_transaction"],
                "last_transaction": r["last_transaction"],
                "active_days": r["active_days"],
                "year": year
            } for r in results
        ]
    
    except Exception as e:
        print(f"Database error in yearly_sales_per_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Quarterly Sales Per Shop
# GET http://127.0.0.1:8000/admin/analytics/quarterly-sales-per-shop-alt?quarter=2&year=2024
@router.get("/quarterly-sales-per-shop-alt", summary="Quarterly Sales Per Shop (Alternative)")
async def get_quarterly_sales_per_shop_alt(
    quarter: int = Query(..., ge=1, le=4, description="Quarter (1-4)"),
    year: int = Query(..., description="Year (e.g., 2024)")
):
    try:
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS quarterly_total,
                COUNT(*) AS transaction_count,
                MIN(transaction_date) AS quarter_start,
                MAX(transaction_date) AS quarter_end,
                COUNT(DISTINCT DATE(transaction_date)) AS active_days
            FROM sales_transactions
            WHERE EXTRACT(QUARTER FROM transaction_date) = {quarter}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY shop_id
            ORDER BY quarterly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "shop_id": str(r["shop_id"]),
                "quarterly_total": float(r["quarterly_total"]),
                "transaction_count": r["transaction_count"],
                "quarter_start": r["quarter_start"],
                "quarter_end": r["quarter_end"],
                "active_days": r["active_days"],
                "quarter": quarter,
                "year": year
            } for r in results
        ]
    
    except Exception as e:
        print(f"Database error in quarterly_sales_per_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Half-Yearly Sales Per Shop
# GET http://127.0.0.1:8000/admin/analytics/half-yearly-sales-per-shop-alt?half=1&year=2024
# GET http://127.0.0.1:8000/admin/analytics/half-yearly-sales-per-shop-alt?half=2&year=2024
@router.get("/half-yearly-sales-per-shop-alt", summary="Half-Yearly Sales Per Shop (Alternative)")
async def get_half_yearly_sales_per_shop_alt(
    half: int = Query(..., ge=1, le=2, description="Half year (1 for Jan-Jun, 2 for Jul-Dec)"),
    year: int = Query(..., description="Year (e.g., 2024)")
):
    try:
        # Determine month range based on half
        if half == 1:
            start_month, end_month = 1, 6
            period_name = "H1"
        else:
            start_month, end_month = 7, 12
            period_name = "H2"
        
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS half_yearly_total,
                COUNT(*) AS transaction_count,
                MIN(transaction_date) AS period_start,
                MAX(transaction_date) AS period_end,
                COUNT(DISTINCT DATE(transaction_date)) AS active_days
            FROM sales_transactions
            WHERE EXTRACT(MONTH FROM transaction_date) >= {start_month}
            AND EXTRACT(MONTH FROM transaction_date) <= {end_month}
            AND EXTRACT(YEAR FROM transaction_date) = {year}
            GROUP BY shop_id
            ORDER BY half_yearly_total DESC
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "shop_id": str(r["shop_id"]),
                "half_yearly_total": float(r["half_yearly_total"]),
                "transaction_count": r["transaction_count"],
                "period_start": r["period_start"],
                "period_end": r["period_end"],
                "active_days": r["active_days"],
                "half": half,
                "period": period_name,
                "year": year
            } for r in results
        ]
    
    except Exception as e:
        print(f"Database error in half_yearly_sales_per_shop_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# Bonus: Top Performing Shops (Configurable Period)
# GET http://127.0.0.1:8000/admin/analytics/top-shops-alt?start_date=2024-01-01&end_date=2024-12-31&limit=10
@router.get("/top-shops-alt", summary="Top Performing Shops in Date Range (Alternative)")
async def get_top_shops_alt(
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
    limit: int = Query(10, ge=1, le=100, description="Number of top shops to return (1-100)")
):
    try:
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        query = f"""
            SELECT 
                shop_id,
                SUM(total_amount) AS total_sales,
                COUNT(*) AS transaction_count,
                AVG(total_amount) AS avg_transaction_amount,
                MIN(transaction_date) AS first_transaction,
                MAX(transaction_date) AS last_transaction,
                COUNT(DISTINCT DATE(transaction_date)) AS active_days
            FROM sales_transactions
            WHERE transaction_date >= '{start_str}' 
            AND transaction_date <= '{end_str}'
            GROUP BY shop_id
            ORDER BY total_sales DESC
            LIMIT {limit}
        """
        
        results = await database.fetch_all(query)
        
        return [
            {
                "rank": idx + 1,
                "shop_id": str(r["shop_id"]),
                "total_sales": float(r["total_sales"]),
                "transaction_count": r["transaction_count"],
                "avg_transaction_amount": float(r["avg_transaction_amount"]),
                "first_transaction": r["first_transaction"],
                "last_transaction": r["last_transaction"],
                "active_days": r["active_days"]
            } for idx, r in enumerate(results)
        ]
    
    except Exception as e:
        print(f"Database error in top_shops_alt: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


@router.get("/all-sales", summary="All Sales")
async def get_all_sales():
    query = text("""
        SELECT * FROM sales_transactions    
    """)
    results = await database.fetch_all(query)
    return [dict(r) for r in results]  # convert result rows to dicts




# # Method using raw SQL without text() wrapper
# @router.get("/daily-sales-raw", summary="Daily Sales Per Shop (Raw SQL)")
# async def get_daily_sales_raw(date_filter: date = Query(..., description="Date in YYYY-MM-DD format")):
#     try:
#         query = """
#             SELECT shop_id, SUM(total_amount) AS daily_total
#             FROM sales_transactions
#             WHERE transaction_date = $1
#             GROUP BY shop_id
#         """
        
#         results = await database.fetch_all(query, date_filter)
#         return [{"shop_id": str(r["shop_id"]), "daily_total": float(r["daily_total"])} for r in results]
    
#     except Exception as e:
#         print(f"Database error in daily_sales_raw: {e}")
#         raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")


# @router.get("/monthly-sales-raw", summary="Total Sales for the Month (Raw SQL)")
# async def get_monthly_sales_raw(month: int = Query(..., ge=1, le=12), year: int = Query(...)):
#     try:
#         query = """
#             SELECT DATE_TRUNC('month', transaction_date) AS month, SUM(total_amount) AS monthly_total
#             FROM sales_transactions
#             WHERE EXTRACT(MONTH FROM transaction_date) = $1
#             AND EXTRACT(YEAR FROM transaction_date) = $2
#             GROUP BY DATE_TRUNC('month', transaction_date)
#         """
        
#         results = await database.fetch_all(query, month, year)
        
#         if results:
#             return {"month": results[0]["month"], "monthly_total": float(results[0]["monthly_total"])}
#         return {"message": "No sales data found for the given month."}
    
#     except Exception as e:
#         print(f"Database error in monthly_sales_raw: {e}")
#         raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")