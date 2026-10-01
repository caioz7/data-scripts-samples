# Apenas um script simples para testar se o Spark está funcionando no ambiente
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TesteSpark").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

dados = [
    ("Brasil", "Paraná", "Curitiba"),
    ("Brasil", "São Paulo", "São Paulo"),
    ("Estados Unidos", "Califórnia", "São Francisco")
]
colunas = ["pais", "estado", "cidade"]

df = spark.createDataFrame(dados, colunas)

print("Spark está funcionando!")
df.show()

spark.stop()

