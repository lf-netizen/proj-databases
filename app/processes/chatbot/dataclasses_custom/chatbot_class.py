from openai import AsyncOpenAI
from typing import List
import aiohttp
import asyncio

class Chatbot:
    openai_client: AsyncOpenAI
    def __init__(self, data):
        self.openai_client = data.pop('openai_client', None)

    async def answer(self, system: str, user: str):
        async for chunk in await self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
                      stream=True):
            current_content = chunk.choices[0].delta.content
            if current_content:
                yield current_content

class PromptFiller:
    async def prepare_question(self, question: str):
        qdrant_result = await self.__qdrant_search(question)
        mongo_result = await self.__search_mongo(qdrant_result)
        return self.__fill_prompt(question, mongo_result)
    
    async def get_names(self, question:str):
        qdrant_result = await self.__qdrant_search(question)
        mongo_result = await self.__search_mongo(qdrant_result)
        return mongo_result

    def __fill_prompt(self, question: str, jsons: List[str]) -> List[str]:
        SYSTEM_TEMPLATE = """You are a professional flower shop assistant, you recommend products that fulfill
        every user expectation or answer their question based only on the data in the JSON format below:
        {}
        Always check the quantity before recommending. If it's equal to 0, ask to wait until restock.
        If none of the products fulfill expectations, say that sadly we don't have the product you need.
        Your answer should be long and contain only the flower you recommend, reasoning why, and a friendly insight.
        Don't encourage further conversation.
        """
        filled_prompt = SYSTEM_TEMPLATE.format(jsons)
        return filled_prompt, question

    async def __qdrant_search(self, question: str):
        async with aiohttp.ClientSession() as session:
            async with session.post("http://api:8000/products/vec_search/", json={'question': question}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    raise Exception(f"Error {response.status}: {error_message}")

    async def __fetch_product(self, session, flower_id):
        async with session.get(f"http://api:8000/products/{flower_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                raise Exception(f"Error {response.status}: {error_message}")

    async def __search_mongo(self, results):
        all_jsons = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for res in results:
                flower_id = res.get('payload').get("id")
                tasks.append(self.__fetch_product(session, flower_id))

            products = await asyncio.gather(*tasks)
            for item in products:
                json_data = {
                    'Name': item.get('name'),
                    'Description': item.get('description'),
                    'Quantity': item.get('quantity')
                    }
                all_jsons.append(json_data)

        return all_jsons

