import gradio as gr
import requests
import time
import io
from PIL import Image

BACKEND_URL = "http://localhost:8000"


# Endpoint para obtener los resultados de la tarea de imagen
def get_task_result(task_id):
    try:
        response = requests.get(f"{BACKEND_URL}/tasks/{task_id}/result")
        response.raise_for_status()
        data = response.json()
        return data.get("status"), data.get("categories", []), data.get("products", [])
    except Exception as e:
        return "failed", str(e), []
    
def handle_search(query, image):
    
    if query and image is not None:
        cat_text, prod_text = search_text(query)
        cat_img, prod_img = process_image(image)
        categories = list(set(cat_text + cat_img))
        products = prod_text + prod_img
        

    elif query:
        categories, products = search_text(query)
     
    elif image is not None:
        categories, products = process_image(image)
    
    else:
        resp = requests.get(f"{BACKEND_URL}/products")
        resp.raise_for_status()
        return [], resp.json().get("products", [])
    
    
    product_names = [p["name"] for p in products if "name" in p]
    return categories, product_names


############################### TEXT ###############################
# Endpoint para la búsqueda de productos basada en texto
def search_text(query):
    try:
        response = requests.post(f"{BACKEND_URL}/search/text", json={"query": query})
        response.raise_for_status()
        return response.json().get("categories", []), response.json().get("products", [])
    except Exception as e:
        return str(e), []


############################### IMAGE ###############################
# Función que gestiona la búsqueda por imagen
def process_image(image):

    task_id = search_image(image)

    attempts = 0
    while attempts < 5:
        if task_id:
            status, categories, products = get_task_result(task_id)
            if status == "completed":
                return categories, products
            elif status == "pending":
                attempts += 1
                time.sleep(1)
                continue
            elif status == "testing":
                return ["Testing"], []
            elif status == "failed":
                return ["Predicción fallida"], []
    return ["Tarea sin respuesta"], []


# Endpoint para la búsqueda de productos basada en imagen
def search_image(image_gr):
    try:
        image_pil = Image.fromarray(image_gr.astype("uint8"))
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        
        
        files = {'file': (io.BytesIO(image_bytes))}
        response = requests.post(f"{BACKEND_URL}/search/image", files=files)
        response.raise_for_status()
        task_id = response.json().get("task_id")
        return task_id
    
    except Exception as e:
        return str(e)
    


if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("## Buscador de Productos (por texto o imagen)")

        with gr.Row():
            query_input = gr.Textbox(label="Describe un producto", placeholder="Ej: zapatillas negras deportivas")
            image_input = gr.Image(label="Sube una imagen", type="numpy")
        
        search_button = gr.Button("Buscar")
        
        with gr.Row():
            output_categories = gr.Textbox(label="Categorías Predichas", value="")
            output_products = gr.List(label="Productos Recomendados", value=[])

        search_button.click(
            fn=handle_search,
            inputs=[query_input, image_input],
            outputs=[output_categories, output_products]
        )

    demo.launch()