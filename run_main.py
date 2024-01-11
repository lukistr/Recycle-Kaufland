from streamlit.web import cli
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

if __name__ == '__main__':
    cli._main_run_clExplicit(file='main.py', command_line='streamlit run')
