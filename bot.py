import streamlit as st



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st
import concurrent.futures



def enviar_email(destinatario, assunto, corpo, arquivo_anexo=None):
    # Configurações do servidor do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Usamos a porta 587 para TLS

    # Informações da conta do Gmail
    remetente = 'ricardosantossar@gmail.com'
    senha = 'ogbbkoirlepnbcah'

    # Criar o objeto do e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    # Adicionar o corpo do e-mail
    msg.attach(MIMEText(corpo, 'plain'))

    # Adicionar o anexo, caso exista
    if arquivo_anexo:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(arquivo_anexo.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{arquivo_anexo.name}"')
        msg.attach(part)

    # Conectar ao servidor do Gmail usando TLS
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remetente, senha)

        # Enviar o e-mail
        server.sendmail(remetente, destinatario, msg.as_string())

    except Exception as e:
        st.error(f'Erro ao enviar o e-mail: {e}')

    finally:
        server.quit()

# Função para enviar a quantidade especificada de e-mails para o mesmo destinatário simultaneamente
def enviar_emails_em_lote(destinatario, assunto, corpo, arquivo_anexo=None, quantidade_por_vez=10):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for _ in range(quantidade_por_vez):
            futures.append(executor.submit(enviar_email, destinatario, assunto, corpo, arquivo_anexo))
        concurrent.futures.wait(futures)

# Definindo as sessões para cada aba
def botmail():
    st.title('Envio de E-mails em Lote')

    # Entrada do destinatário
    st.subheader('Insira o destinatário:')
    destinatario = st.text_input('Destinatário', '')

    # Assunto e corpo do e-mail
    assunto = st.text_input('Assunto do e-mail', 'Assunto padrão')
    corpo = st.text_area('Corpo do e-mail', 'Conteúdo do e-mail')

    # Upload do arquivo em anexo
    uploaded_file = st.file_uploader('Selecione um arquivo para anexar', type=['pdf', 'png', 'jpg', 'jpeg', 'gif'])

    # Escolha da quantidade de e-mails a enviar por vez
    quantidade_por_vez = st.slider('Quantidade de e-mails por vez', min_value=1, max_value=100, value=10)

    # Botão para enviar os e-mails
    if st.button('Enviar E-mails'):
        if destinatario.strip() != '':
            # Verificar se foi feito upload de um arquivo
            arquivo_anexo = uploaded_file if uploaded_file is not None else None
            enviar_emails_em_lote(destinatario, assunto, corpo, arquivo_anexo, quantidade_por_vez)
            st.success('E-mails enviados com sucesso!')
        else:
            st.warning('Insira um destinatário válido.')


def gerar_mensagem_whatsapp():
    nome_empresa = "Fotus Energia Solar"

    nota_fiscal = st.text_input("Número da Nota Fiscal:")
    destinatario = st.text_input("Nome do destinatário:")
    data_agendamento = st.text_input("Data do agendamento:")
    pedido = st.text_input("Número do pedido:")
    motorista = st.text_input("Nome do motorista:")

    mensagem_gerada = f"Meu nome é Ricardo, falo da {nome_empresa}.\n"
    mensagem_gerada += f"Estamos com uma entrega referente à NF {nota_fiscal} do destinatário {destinatario},\n"
    mensagem_gerada += f"gostaria de agendar a entrega para o dia {data_agendamento}.\n"
    mensagem_gerada += f"Detalhes do pedido: {pedido}.\n"
    mensagem_gerada += f"Motorista responsável: {motorista}.\n"

    return mensagem_gerada

# Função principal da aba "Bozap"
def bozap():
    st.title("Bozap")
    st.write("Bem-vindo(a) à aba Bozap!")
    st.write("Aqui você pode gerar uma mensagem para WhatsApp.")
    
    mensagem_gerada = gerar_mensagem_whatsapp()

    st.markdown("**Texto gerado:**")
    st.text_area("", mensagem_gerada, height=200, max_chars=None, key=None)

    numero_whatsapp = st.text_input("Insira o número de WhatsApp do destinatário (inclua o DDI, ex.: +55):")

    if st.button("Gerar Link para WhatsApp"):
        mensagem_codificada = quote(mensagem_gerada)
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensagem_codificada}"
        st.markdown(f"**Link para enviar a mensagem:**")
        st.markdown(f"[{link_whatsapp}]({link_whatsapp})")

def botBlaze():
    st.title('BotBlaze')
    # Conteúdo da aba "BotBlaze"
    st.write("Conteúdo da aba BotBlaze.")

def main():
    st.sidebar.title('Menu')
    opcoes = ['Botmail', 'Bozap', 'BotBlaze']
    aba_selecionada = st.sidebar.selectbox('Selecione a aba:', opcoes)

    if aba_selecionada == 'Botmail':
        botmail()
    elif aba_selecionada == 'Bozap':
        bozap()
    elif aba_selecionada == 'BotBlaze':
        botBlaze()

if __name__ == '__main__':
    main()
