from sentence_transformers import SentenceTransformer
from qdrant_client import AsyncQdrantClient
from models.product import Product, VecProduct
from qdrant_client.models import Filter, FieldCondition, PointStruct, MatchValue, PointVectors

class QdrantManager:
    qdrant_client: AsyncQdrantClient
    modelEmbed: SentenceTransformer

    def __init__(self) -> None:
        self.qdrant_client = AsyncQdrantClient('http://qdrant:6333')
        self.modelEmbed = SentenceTransformer('intfloat/e5-small-v2', cache_folder='src/model_st')
        pass

    async def search(self, query:str):
        vector = self.modelEmbed.encode(query, normalize_embeddings=True)
        response = await self.qdrant_client.search(collection_name="products_description",
                                          query_vector=vector,
                                          limit=3,
                                          query_filter= Filter(
                                              must=[
                                                  FieldCondition(
                                                      key='is_enabled',
                                                      match = MatchValue(value=True)
                                                  )
                                              ]
                                          ))
        return response

    async def add_product_vec(self,product: Product):
        if not await self.__check_db__(product.name):
            vector = self.modelEmbed.encode(product.description,normalize_embeddings=True)
            num = await self.qdrant_client.count(collection_name="products_description")
            point = PointStruct(
                        id=int(num.count),
                        vector=vector,
                        payload={"id": product.id, "name": product.name, 
                                 "description": product.description, 
                                 "is_enabled": product.is_enabled}
                    )

            await self.qdrant_client.upsert(
                collection_name="products_description",
                wait=True,
                points=[point])
        else:
            print('Product already exists')

    async def update_product(self,product: Product):
        product_in_base = await self.__check_db__(product.name)
        if product.is_enabled:
            updated_product = VecProduct(**product_in_base.payload)
            updated_product.description = product.description
            vector = self.modelEmbed.encode(product.description,normalize_embeddings=True)
            updated_product.is_enabled = product.is_enabled
            payload=dict(updated_product)
            await self.qdrant_client.update_vectors(
                collection_name='products_description',
                points = [
                    PointVectors(
                    id=int(product_in_base.id),
                    vector=vector,
                )
                ]
            )
        else:
            updated_product = VecProduct(**product_in_base.payload)
            updated_product.is_enabled = product.is_enabled
            # point = PointVectors(
            #         id=int(product_in_base.id),
            #         vector=product_in_base.vector,
            #         payload=dict(updated_product)
            # )
            payload=dict(updated_product)
        await self.qdrant_client.overwrite_payload(
            collection_name="products_description",
            wait = True,
            points=Filter(must=[FieldCondition(
                            key='name',
                            match = MatchValue(value=updated_product.name)
            )]),
            payload=payload
        )

    async def __check_db__(self,name):
        record = await self.qdrant_client.scroll(
        collection_name ="products_description",
        scroll_filter = Filter(
            must = [FieldCondition(
                key='name',
                match =MatchValue(
                    value= name))
                    ]
                ),
                with_vectors = True
            )
        if record[0]:
            return record[0][0]
        else:
            return False

