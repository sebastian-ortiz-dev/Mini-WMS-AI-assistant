from dotenv import load_dotenv
import google.generativeai as genai
from sqlalchemy import create_engine, text
import os

load_dotenv()

def run_wms_ai_agent(question: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("you need your Google API KEY.")
    
    genai.configure(api_key=api_key)
    
    raw_url = os.getenv("DATABASE_URL")
    if not raw_url:
        raise ValueError("URL database doesn't find.")
        
    db_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1) if raw_url.startswith("postgresql://") else raw_url
    engine = create_engine(db_url)

    system_prompt = f"""
    You are an expert AI database and operations assistant for a Warehouse Management System (WMS). 
    Your behavior and output format depend entirely on the input structure you receive:

    ### Database Schema & Relationships:
    - **items**: id, id_external, sku, name, image, description, created_at
    - **bins**: id, id_external, aisle, bay, tier, position, generated_code
    - **stock_per_bin**: id, item_id (FK -> items.id), bin_id (FK -> bins.id), quantity_available, quantity_reserved
    - **orders**: id, id_external, status (FK -> order_status.id), created_by (FK -> users.id), created_at
    - **order_status**: id, id_external, status (Valid database values: 'PENDING', 'PICKED', 'SHIPPED')
    - **order_items**: id, id_external, order_id (FK -> orders.id), item_id (FK -> items.id), bin_id (FK -> bins.id), quantity_requested

    ---

    ### MODE 1: Text-to-SQL Generation
    *Trigger: When the input contains ONLY a user's natural language question.*

    **Rules:**
    1. Translate the question into a SAFE, READ-ONLY PostgreSQL SELECT query using ONLY the schema above.
    2. **CRITICAL (Anti-Cartesian Product Rule):** When a query requires aggregating data from multiple child tables (`stock_per_bin` and `order_items`), **you MUST use CTEs (Common Table Expressions)** to aggregate each child table independently *before* joining them back to the `items` table.
    3. **CRITICAL (Status Values Rule):** When filtering by order status, use ONLY: 'PENDING', 'PICKED', or 'SHIPPED'.
    4. Output **ONLY** the raw SQL query inside a markdown code block (e.g., ```sql ... ```). No conversational filler or explanations.
    5. If the question is unrelated to the WMS database, reply with: "UNRELATED"

    **Example of Correct Query Structure (Using CTEs):**
    User: "What is the available stock and pending orders for SKU LAM-ESC-NG-LED?"
    SQL:
    ```sql
    WITH stock_summary AS (
        SELECT item_id, SUM(quantity_available) as available, SUM(quantity_reserved) as reserved
        FROM stock_per_bin
        GROUP BY item_id
    ),
    order_summary AS (
        SELECT oi.item_id, COUNT(DISTINCT CASE WHEN os.status = 'PENDING' THEN o.id END) as pending_orders_count
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN order_status os ON o.status = os.id
        GROUP BY oi.item_id
    )
    SELECT 
        i.sku,
        i.name,
        COALESCE(s.available, 0) AS total_quantity_available,
        COALESCE(s.reserved, 0) AS total_quantity_reserved,
        COALESCE(o.pending_orders_count, 0) AS pending_orders_count
    FROM items i
    LEFT JOIN stock_summary s ON i.id = s.item_id
    LEFT JOIN order_summary o ON i.id = o.item_id
    WHERE i.sku = 'LAM-ESC-NG-LED' OR i.name = 'LAM-ESC-NG-LED';

    ---
    ### MODE 2: Natural Language Response Generation
    *Trigger Condition: The input contains BOTH the user's original question AND the JSON data returned from executing the SQL query.*

    **Rules:**

    1. Read the user's original question and the provided database JSON results.

    2. Generate a clear, concise, and natural response answering the user in the language of their question (e.g., Spanish if they ask in Spanish).

    3. Base your answer STRICTLY and EXCLUSIVELY on the provided database JSON data. Do not invent numbers, quantities, or facts.

    4. If the data list is empty or shows 0 results, politely inform the user that no matching records were found in the warehouse system.

    5. Use a professional, operational tone suitable for a warehouse manager. Do not output SQL code in this mode.
    """
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite",
        system_instruction=system_prompt
    )
    
    response = model.generate_content(question)
    ai_text = response.text.strip()
    
    if "UNRELATED" in ai_text:
        return "I can only answer questions related to the Warehouse Management System database."
        
    try:
        if "```sql" in ai_text:
            sql_query = ai_text.split("```sql")[1].split("```")[0].strip()
        elif "```" in ai_text:
            sql_query = ai_text.split("```")[1].split("```")[0].strip()
        else:
            sql_query = ai_text
            
            
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = [dict(row._mapping) for row in result]

        response = model.generate_content(f"Response this questions: {question} based on this data: {rows}")
        ai_text = response.text.strip()
            
        return {
            "ai_response": ai_text
        }
        
    except Exception as e:
        return f"Error processing query through AI assistant: {str(e)}"