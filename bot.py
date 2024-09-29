import os
import random
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Define the SlimIAData class
class SlimIAData:
    # (Copy the entire implementation from slim_ia_data.py here)
def carregar_conteudo_arquivo():
    # Abre e lê o conteúdo do arquivo
    with open("conteudo_site.txt", "r", encoding="utf-8") as file:
        conteudo = file.read()

    # Dividir o conteúdo com base nos títulos das seções
    secoes = conteudo.split("\n\n")  # Ajuste conforme a formatação do seu arquivo
    conteudo_dict = {}

    # Identificar e categorizar as seções
    for secao in secoes:
        if "Mentalidade" in secao:
            conteudo_dict["mentalidade"] = secao
        elif "Alimentação" in secao:
            conteudo_dict["alimentacao"] = secao
        # Continue categorizando as outras seções conforme necessário

    return conteudo_dict

def obter_secao(secao):
    conteudo = carregar_conteudo_arquivo()
    return conteudo.get(secao, "Seção não encontrada.")

class SlimIAData:
    def __init__(self):
        # Identidade da assistente
        self.identity = (
            "Você é a assistente oficial do Projeto Super Slim, chamada SLIM IA. "
            "Estou aqui para acompanhar e apoiar as participantes na jornada de emagrecimento, "
            "compartilhando conhecimento sobre saúde, ajudando a criar estratégias personalizadas "
            "com base nos pilares do projeto e incentivando a comunicação e o suporte mútuo entre todas."
        )

        # Pilares do projeto
        self.pilares = {
            "mentalidade": {
                "descricao": "Desenvolver uma perspectiva positiva em relação à perda de peso, tornando-a uma experiência agradável.",
                "exemplos": [
                    "Praticar a gratidão diariamente.",
                    "Definir metas realistas e comemorá-las.",
                ],
                "dicas": [
                    "Mantenha um diário de pensamentos positivos.",
                    "Evite comparações com outras pessoas."
                ],
                "erros_comuns": [
                    "Pensar que a perda de peso deve ser rápida.",
                    "Desvalorizar pequenas conquistas."
                ]
            },
            "alimentação": {
                "descricao": "Promover um equilíbrio nutricional em vez de dietas restritivas, focando em hábitos alimentares sustentáveis.",
                "exemplos": [
                    "Incluir mais frutas e vegetais nas refeições.",
                    "Fazer refeições em casa em vez de comer fora."
                ],
                "dicas": [
                    "Hidratar-se adequadamente.",
                    "Evitar pular refeições."
                ],
                "erros_comuns": [
                    "Eliminar grupos alimentares inteiros.",
                    "Focar apenas em calorias."
                ]
            },
            "movimentação": {
                "descricao": "Incentivar a atividade física integrada de forma natural na rotina diária, vista como uma escolha de estilo de vida positiva.",
                "exemplos": [
                    "Caminhar ou andar de bicicleta para o trabalho.",
                    "Participar de aulas de dança ou esportes."
                ],
                "dicas": [
                    "Encontrar uma atividade que você goste.",
                    "Fazer pequenas pausas para se mover durante o dia."
                ],
                "erros_comuns": [
                    "Pular dias de atividade física.",
                    "Comparar-se com o desempenho dos outros."
                ]
            },
            "suplementação": {
                "descricao": "Apresentar suplementos como auxílios complementares em vez de substitutos para uma dieta equilibrada e exercício.",
                "exemplos": [
                    "Usar suplementos vitamínicos quando necessário.",
                    "Consultar um nutricionista antes de começar a tomar qualquer suplemento."
                ],
                "dicas": [
                    "Priorizar alimentos integrais e naturais.",
                    "Informar-se sobre os suplementos que você está considerando."
                ],
                "erros_comuns": [
                    "Dependência excessiva de suplementos.",
                    "Negligenciar a alimentação saudável."
                ]
            },
            "comunicação": {
                "descricao": "Fomentar a interação da comunidade entre participantes para motivação e suporte.",
                "exemplos": [
                    "Participar de grupos de apoio.",
                    "Compartilhar progressos nas redes sociais."
                ],
                "dicas": [
                    "Ouvir e apoiar outras participantes.",
                    "Ser aberto sobre seus desafios e sucessos."
                ],
                "erros_comuns": [
                    "Isolar-se durante a jornada.",
                    "Não buscar ajuda quando necessário."
                ]
            }
        }

        # Informações adicionais sobre o projeto
        self.informacoes_adicionais = (
            "O Projeto Super Slim é uma plataforma gratuita dedicada à perda de peso feminina, "
            "estruturada em torno de cinco pilares essenciais. Os participantes são incentivados a "
            "definir metas e realizar tarefas diárias personalizadas para alcançar seus objetivos."
        )

        # Perguntas frequentes (FAQ)
        self.faq = {
            "Quais são os benefícios da atividade física?": "A atividade física ajuda a melhorar a saúde física e mental, aumenta a energia, e auxilia na manutenção do peso.",
            "Como posso manter a motivação?": "Defina metas pequenas, celebre suas conquistas e procure apoio de amigos e familiares.",
            "O que fazer se eu tiver um dia de deslize?": "É normal ter deslizes. Foque em voltar aos seus hábitos saudáveis no dia seguinte."
        }

        # Mensagens motivacionais
        self.mensagens_motivacionais = [
            "Você é mais forte do que imagina.",
            "Cada passo conta, mesmo os pequenos.",
            "A mudança leva tempo, mas cada esforço vale a pena.",
            "Acredite em você e nos seus objetivos!",
            "Você está fazendo progresso todos os dias."
        ]

    # Métodos para obter informações sobre os pilares
    def get_pilares_info(self):
        return "\n".join([f"{pilar.capitalize()}: {info['descricao']}" for pilar, info in self.pilares.items()])

    def get_dicas_pilar(self, pilar):
        return "\n".join(self.pilares[pilar]["dicas"]) if pilar in self.pilares else "Pilar não encontrado."

    def get_erros_comuns_pilar(self, pilar):
        return "\n".join(self.pilares[pilar]["erros_comuns"]) if pilar in self.pilares else "Pilar não encontrado."

    # Método para obter todas as informações
    def get_all_info(self):
        return f"{self.identity}\n\n{self.informacoes_adicionais}\n\nPilares do Projeto:\n{self.get_pilares_info()}"

    # Método para obter perguntas frequentes
    def get_faq(self):
        return "\n".join([f"{pergunta}: {resposta}" for pergunta, resposta in self.faq.items()])

    # Método para obter uma mensagem motivacional aleatória
    def get_mensagem_motivacional(self):
        return random.choice(self.mensagens_motivacionais)

# Create an instance of SlimIAData
slim_ia_data = SlimIAData()

# Configurar os tokens a partir das variáveis de ambiente
API_GITHUB_TOKEN = os.getenv("API_GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configurar a API do OpenAI
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=API_GITHUB_TOKEN,
)

# Instancia a classe que contém as informações
slim_ia_data = SlimIAData()

async def get_openai_response(message: str) -> str:
    try:
        # Usa a informação da SLIM IA para responder
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": slim_ia_data.get_all_info()},
                {"role": "user", "content": message},
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Desculpe, houve um erro: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou a SLIM IA, sua assistente. Como posso ajudá-lo hoje?')

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = await get_openai_response(user_message)
    await update.message.reply_text(response)

def main() -> None:
    # Criar a aplicação
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Adicionar handlers de comando
    app.add_handler(CommandHandler("start", start))

    # Adicionar handler de mensagens
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Iniciar polling
    app.run_polling()

if __name__ == "__main__":
    main()
