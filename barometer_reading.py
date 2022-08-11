from datetime import datetime as dt

from bs4 import BeautifulSoup
from pyvisa import ResourceManager


HTML_FILE = r'./current_pressure_reading.html'
BAROMETER_ADDRESS = 'SOME_IP_ADDRESS'
rm = ResourceManager('@py')

with rm.open_resource(f"TCPIP::{BAROMETER_ADDRESS}::inst0::INSTR") as druck:
    pressure_reading = float(druck.query(':SENSe:PRESsure?').split()[1])

measurement_text = f'Pressure {pressure_reading:.2f}&nbsp;mmHg ({pressure_reading / 0.7501 :.2f}&nbsp;hPa), current as of {dt.now().replace(microsecond=0)}'

with open(HTML_FILE) as fp:
    soup = BeautifulSoup(fp, 'html.parser')

pressure_para = soup.find("p", {"id":"pressure"})
pressure_para.string = measurement_text

with open(HTML_FILE, "wb") as f_output:
    f_output.write(soup.prettify("utf-8", formatter=None))