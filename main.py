import streamlit as st
import pandas as pd
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import subprocess
from datetime import datetime
import warnings
from colorama import Fore
import streamlit_option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

st.markdown("""
    <style>
        .st-emotion-cache-18ni7ap {
            display: none;
        }
        .big-font {
            font-size: 2rem !important;
        }
        .header-text {
            color: #2c3e50;
        }
        .submit-button {
            background-color: #2980b9;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .block-container, .st-emotion-cache-1y4p8pa, .ea3mdgi2{
            padding-top: 0;
            display: inline-block;
        }
        .block-container, .st-emotion-cache-1y4p8pa {
            max-width: 100%;
            padding-top: 0;
        }
        .st-emotion-cache-10trblm {
            text-align: center;
        }
        .element-container, .st-emotion-cache-1vzq8hd, .st-emotion-cache-11on9qe {
            text-align: center;
            display: block;
        }
        .st-emotion-cache-keje6w, .e1f1d6gn3{
            padding: 0 8% 0 8%;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
        }
        .inline {
            width: 48%;
        }
        .stSelectbox {
            text-align: center;
            max-width: 30%;
            width: 30%;
            display: inline-block;
        }
        .st-emotion-cache-kskxxl{
            max-width: 250px;
        }
        .e1f1d6gn4 {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .stDateInput, .stNumberInput {
            max-width: 250px;
        }
    </style>
""", unsafe_allow_html=True)

def write_logs(message_logs):
    with open('logs/output.txt', 'a') as file:
        file.write(f'{message_logs}\n')

def create_pdf_bg(reg_number, pdf_file_path, exit_date_truck, exit_time_truck):
    df = pd.read_excel('truck_data.xlsx')
    filtered_row = df.loc[(df['Регистрационен номер'] == reg_number) & (df['Принт'].isna())]
    index = filtered_row.index[0] + 1
    reg_number = filtered_row['Регистрационен номер'].values[0]
    entry_weight = filtered_row['Тегло на вход'].values[0]
    entry_date = filtered_row['Дата на вход'].values[0]
    entry_time = filtered_row['Време на вход'].values[0]
    company = filtered_row['Фирма за рециклиране'].values[0]
    exit_weight = filtered_row['Тегло на изход'].values[0]
    exit_date = filtered_row['Дата на изход'].values[0]
    exit_time = filtered_row['Време на изход'].values[0]
    pdf_file = 'documents/' + company + ' ' + exit_date_truck + ' ' + exit_time_truck + '.pdf'

    pdfmetrics.registerFont(TTFont('Roboto', 'fonts/Roboto-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto_bold', 'fonts/Roboto-Bold.ttf'))
    c = canvas.Canvas(pdf_file, pagesize=A4)

    # Задаване на размера на страницата
    width, height = A4

    # Задаване на стил
    style = getSampleStyleSheet()["BodyText"]
    style.alignment = TA_CENTER
    style.textColor = colors.black
    style.fontName = "Roboto_bold"
    style.fontSize = 18

    # Изчисляване на ширината на текста, за да се намери централната позиция
    text = 'Кауфланд България, с. Стряма'
    text_width = stringWidth(text, style.fontName, style.fontSize)
    x = (width - text_width) / 2.0

    # Изпишете текста в центъра на страницата
    c.setFont(style.fontName, style.fontSize)
    c.setFillColor(style.textColor)
    c.drawString(x, height - (height / 4), text)

    text = 'Измерване №: ' + str(index)
    text_width = stringWidth(text, 'Roboto', 12)
    x = (width - text_width) / 2.0
    c.setFont('Roboto', 12)
    c.drawString(x, height - (height / 4) - 50, text)

    text = 'Рег. №:     ' + str(reg_number).upper()
    c.drawString(100, height - (height / 4) - 85, text)
    text = 'Дата вход:     ' + str(entry_date)
    c.drawString(100, height - (height / 4) - 110, text)
    text = 'Дата изход:    ' + str(exit_date)
    c.drawString(330, height - (height / 4) - 110, text)
    text = 'Час вход:        ' + str(entry_time)
    c.drawString(100, height - (height / 4) - 130, text)
    text = 'Час изход:       ' + str(exit_time)
    c.drawString(330, height - (height / 4) - 130, text)
    text = 'Име на фирма: ' + str(company)
    c.drawString(100, height - (height / 4) - 170, text)
    text = 'Тара:                          ' + str(entry_weight)
    c.drawString(100, height - (height / 4) - 225, text)
    text = 'Тегло на изход:       ' + str(exit_weight)
    c.drawString(100, height - (height / 4) - 245, text)
    text = 'Нето тегло:               ' + str((int(exit_weight) - int(entry_weight)))
    c.drawString(100, height - (height / 4) - 265, text)
    text = 'Оператор:               Кауфланд България'
    c.drawString(100, height - (height / 4) - 310, text)

    # Покажете първата страница
    c.showPage()

    c.drawImage('Logo.png', width - 110, height - 110, 100, 100)

    # Задаване на стил
    style = getSampleStyleSheet()["BodyText"]
    style.alignment = TA_CENTER
    style.textColor = colors.black
    style.fontName = "Roboto_bold"
    style.fontSize = 20

    # Изчисляване на ширината на текста, за да се намери централната позиция
    text = 'Приемо - Предавателен Протокол'
    text_width = stringWidth(text, style.fontName, style.fontSize)
    x = (width - text_width) / 2.0

    # Изпишете текста в центъра на страницата
    c.setFont(style.fontName, style.fontSize)
    c.setFillColor(style.textColor)
    c.drawString(x, height - (height / 6) - 10, text)

    c.setFont('Roboto', 12)
    text = 'Днес ' + str(exit_date)
    c.drawString(70, height - (height / 4), text)
    text = '"Кауфланд България енд Ко КД", предава на представител на фирма '
    c.drawString(70, height - (height / 4) - 30, text)
    text = str(company).upper() + ' за рециклиране:'
    c.drawString(70, height - (height / 4) - 55, text)
    text = '.............................................................. - .................... бр. с тегло ' + str((int(exit_weight) - int(entry_weight))) + ' кг.'
    c.drawString(70, height - (height / 4) - 85, text)
    text = 'Приел: .......................................................'
    c.drawString(width - 270, height - (height / 2), text)
    c.setFont('Roboto', 9)
    text = '/фамилия и подпис/'
    c.drawString(width - 180, height - (height / 2) - 12, text)
    c.setFont('Roboto', 12)
    text = 'Предал: ......................................................'
    c.drawString(width - 270, height - (height / 2) - 50, text)
    c.setFont('Roboto', 9)
    text = '/фамилия и подпис/'
    c.drawString(width - 180, height - (height / 2) - 62, text)
    c.setFont('Roboto', 12)
    text = 'Централен склад'
    c.drawString(70, height - (height / 2) - 150, text)
    text = 'с. Стряма (инд. зона Раковски)'
    c.drawString(70, height - (height / 2) - 170, text)

    c.save()
    last_entry_index = df[(df['Регистрационен номер'] == reg_number) & (df['Принт'].isna())].index[-1]
    df.at[last_entry_index, 'Принт'] = 'Принтиран'
    df.to_excel(pdf_file_path, index=False, engine='openpyxl')

    print_pdf_doc(pdf_file)

def security_page_create():
    with st.form(key='dual_column_form', clear_on_submit=True):
        # Използваме стилове, за да подредим полетата в две колони
        col1, col2 = st.columns(2)

        # Първа колона
        with col1:
            st.markdown('<p class="normal-font">Вход</p>', unsafe_allow_html=True)
            registration_number = st.text_input('Регистрационен номер:', value="", key='registration_number')
            entry_weight = st.text_input('Тегло на вход:', value="", key='entry_weight')
            company = st.text_input('Фирма за рециклиране:', value="", key='company')
            submit_entry = st.form_submit_button(label='Потвърди вход')
            if submit_entry:
                current_date = datetime.now().strftime('%d.%m.%Y')
                current_time = datetime.now().strftime('%H:%M:%S')
                excel_path = 'truck_data.xlsx'
                df = pd.read_excel(excel_path)

                new_entry = pd.DataFrame({
                    'Регистрационен номер': [registration_number],
                    'Тегло на вход': [entry_weight],
                    'Фирма за рециклиране': [company],
                    'Тегло на изход': [''],
                    'Статус': ['In'],
                    'Дата на вход': [current_date],
                    'Време на вход': [current_time],
                    'Дата на изход': [''],
                    'Време на изход': [''],
                    'Принт': [''],
                    'Име на файла': ['']
                })

                df = pd.concat([df, new_entry], ignore_index=False)
                df.to_excel(excel_path, index=False, engine='openpyxl')

                st.success('Входните данни са потвърдени успешно!')

                message_log_entry = f'{datetime.now()}: Камион с регистрационен номер {registration_number} влиза в Централен склад.'
                print(Fore.YELLOW + message_log_entry + Fore.RESET)
                write_logs(message_log_entry)

        # Втора колона
        with col2:
            try:
                st.markdown('<p class="normal-font">Изход</p>', unsafe_allow_html=True)
                exit_registration_number = st.text_input('Регистрационен номер за изход:', value="", key='exit_registration_number')
                exit_weight = st.text_input('Изходно тегло:', value="", key='exit_weight')
                submit_exit = st.form_submit_button(label='Потвърди изход')
                if submit_exit:
                    current_date = datetime.now().strftime('%d.%m.%Y')
                    current_time = datetime.now().strftime('%H:%M:%S')
                    exit_date = datetime.now().strftime('%Y_%m_%d')
                    exit_time = datetime.now().strftime('%H_%M_%S')
                    excel_path = 'truck_data.xlsx'
                    df = pd.read_excel(excel_path)
                    last_entry_index = df[(df['Регистрационен номер'] == exit_registration_number) & (df['Статус'] == 'In')].index[-1]
                    df.at[last_entry_index, 'Тегло на изход'] = int(exit_weight)
                    df.at[last_entry_index, 'Статус'] = 'Out'
                    df.at[last_entry_index, 'Дата на изход'] = str(current_date)
                    df.at[last_entry_index, 'Време на изход'] = str(current_time)
                    filtered_row = df.loc[(df['Регистрационен номер'] == exit_registration_number)]
                    company = filtered_row['Фирма за рециклиране'].values[0]
                    df.at[last_entry_index, 'Име на файла'] = company + ' ' + exit_date + ' ' + exit_time + '.pdf'
                    df.to_excel(excel_path, index=False, engine='openpyxl')
                    st.success('Успешен изход!')

                    message_log_leave = f'{datetime.now()}: Камион с регистрационен номер {exit_registration_number} напуска Централен склад.'
                    print(Fore.GREEN + message_log_leave + Fore.RESET)
                    write_logs(message_log_leave)

                    create_pdf_bg(exit_registration_number, excel_path, exit_date, exit_time)
                    security_page_create()
            except Exception as e:
                print(f'Игнорирана грешка {e}')

    # Показване на текущите данни в Excel файл
    st.markdown('<p class="big-font">Камиони с вход</p>', unsafe_allow_html=True)
    current_data = pd.read_excel('truck_data.xlsx')
    filtered_data = current_data[current_data['Статус'] == 'In']  # Филтриране на само активните камиони
    st.write(filtered_data)

def print_pdf_doc(pdf_name):
    try:
        # Отваряме PDF файла със стандартната програма за преглед на PDF
        subprocess.Popen([pdf_name], shell=True)
    except Exception as e:
        message_log_error = Fore.RED + f"{datetime.now()}: Грешка при отваряне на файла: {e}" + Fore.RESET
        print(message_log_error)
        write_logs(message_log_error)

def check_create_file(x_file_path):
    headers = [
        'Регистрационен номер',
        'Тегло на вход',
        'Фирма за рециклиране',
        'Тегло на изход', 'Статус',
        'Дата на вход',
        'Време на вход',
        'Дата на изход',
        'Време на изход',
        'Принт',
        'Име на файла'
    ]

    wb = Workbook()
    ws = wb.active
    # Задаваме стойности за заглавия
    for col_num, header in enumerate(headers, 1):
        ws.cell(row=1, column=col_num, value=header)

    # Запазваме промените
    wb.save(x_file_path)

def select_page():
    selected = streamlit_option_menu.option_menu(
        menu_title=None,
        options=['Охрана', 'ЕДВ'],
        icons=['truck', 'wrench-adjustable'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal',
    )

    if selected == 'Охрана':
        security_page_create()
    elif selected == 'ЕДВ':
        login_form()
    else:
        security_page_create()

def edv_page_create():
    st.markdown('<p class="big-font">Камиони с вход за дата</p>', unsafe_allow_html=True)
    search_date = st.date_input('Въведете дата', value=datetime.now(), format='DD.MM.YYYY', key='edv-search-date')
    formatted_date = search_date.strftime('%d.%m.%Y')
    current_data = pd.read_excel('truck_data.xlsx')
    filtered_data = current_data[current_data['Дата на вход'] == formatted_date]
    st.write(filtered_data)

    # Зареждане на екселския файл
    df = pd.read_excel(excel_file_path)

    # Изобразяване на данните за избрания ред
    if len(df) > 0:
        # Добавяне на избор на редове чрез текстово поле
        selected_row = st.number_input("Изберете ред по индекс от файла:", min_value=0, value=0, step=1)
        selected_row = int(selected_row)
        try:
            st.write("Избран ред:", df.iloc[selected_row][['Регистрационен номер', 'Статус', 'Принт', 'Име на файла']])

            # Добавяне на бутон за промяна на статуса
            if st.button("Промени статус"):
                if df.at[selected_row, 'Статус'] == "Out":
                    # Променете статуса на избрания ред
                    df.at[selected_row, 'Статус'] = "In"
                    df.at[selected_row, 'Принт'] = ""
                    st.write('Статуса е променен успешно.')
                else:
                    st.write('Камиона все още не е напуснал склада.')

                # Запазете промените в екселския файл
                df.to_excel(excel_file_path, index=False)
            elif st.button("Принтирай"):
                print_doc = 'documents/' + df.loc[selected_row, 'Име на файла']
                print_pdf_doc(print_doc)
        except IndexError:
            st.write('Избрания ред е празен!')
    else:
        st.write('Екселския файл е празен!')

def login_form():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login(location='main')
    if authentication_status:
        edv_page_create()
        authenticator.logout('Изход', 'main')
    elif not authentication_status:
        st.error('Грешно потребителско име или парола!')
    elif authentication_status is None:
        st.warning('Въведете потребителско име и парола!')

if __name__ == "__main__":
    current_dir = os.getcwd()

    log_dir = 'logs'
    target_log_dir = os.path.join(current_dir, log_dir)
    if not os.path.exists(target_log_dir):
        os.makedirs(target_log_dir)
        message_log = Fore.RESET + f'{datetime.now()}: Папката ' + Fore.LIGHTGREEN_EX + f'{log_dir}' + Fore.RESET + ' беше успешно създадена.'
        print(Fore.LIGHTGREEN_EX + message_log + Fore.RESET)
        write_logs(message_log)

    dir_name = 'documents'
    target_dir = os.path.join(current_dir, dir_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        message_log = Fore.RESET + f'{datetime.now()}: Папката ' + Fore.LIGHTGREEN_EX + f'{dir_name}' + Fore.RESET + ' беше успешно създадена.'
        print(Fore.LIGHTGREEN_EX + message_log + Fore.RESET)
        write_logs(message_log)

    excel_file_path = "truck_data.xlsx"
    if not os.path.exists(excel_file_path):
        check_create_file(excel_file_path)
        message_log = Fore.RESET + f'{datetime.now()}: Файлът ' + Fore.LIGHTGREEN_EX + f'{excel_file_path}' + Fore.RESET + ' беше успешно създаден.'
        print(message_log)
        write_logs(message_log)

    select_page()
