from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
import qdarktheme
# from PyQt5.QtChart import QChart, QPieSeries, QChartView, QLegend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os 
import csv
import time
import requests
from datetime import datetime
from transformers import pipeline
summarizer = pipeline("summarization")

class Ui(qtw.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('layout.ui', self)
        self.positive = 1
        self.negative = 0
        self.neutral = 0
        self.pie_chart = None
        # if self.positive or self.negative or self.neutral:
        #     self.pie_chart = self.create_pie_chart()
        #     self.graphLayout.addWidget(self.pie_chart)
        self.get_csv_btn.clicked.connect(self.process_csv_func)
        self.csv_file_textedit.returnPressed.connect(self.process_csv_func)
        self.export_csv_btn.clicked.connect(self.exportToCSV)
        self.worker_thread = None
        self.worker = None
        self.show()
    
    def process_csv_func(self):
        sender = self.sender()  # Get the button that triggered the function
        if sender:
            if sender == self.get_csv_btn:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.ReadOnly
                file_path, _ = qtw.QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv);;All Files (*)', options=options)

                if file_path:
                    file_path = os.path.normpath(file_path)
                    self.csv_file_textedit.setText(file_path)
                    # print(file_path)
            
        if not os.path.exists(self.csv_file_textedit.text()):
            self.alert_message.setText("csv file not exist !!!")
        else:
            self.csv_file_textedit.setEnabled(False)
            self.get_csv_btn.setEnabled(False)
            self.export_csv_btn.setEnabled(False)
            self.alert_message.setText("")
            if self.worker is not None:
                self.worker.table_data.disconnect()
                self.worker.graph_data.disconnect()
                self.worker_thread.quit()
                self.worker_thread.wait()
                self.result_table.setRowCount(0)
            self.worker= WorkerThread(csv_file_path="sample-input.csv")
            self.worker_thread = qtc.QThread()

            
            

            #connecting signal and slot
            self.worker.table_data.connect(self.update_table)
            self.worker.graph_data.connect(self.update_graph)

            #assign worker to thread
            self.worker.moveToThread(self.worker_thread)
            # Connect the thread's started signal to the run method of the WorkerThread
            self.worker_thread.started.connect(self.worker.run)
            self.worker_thread.finished.connect(self.enable_widgets)
            # Connect the thread's finished signal to a method that will remove the worker
            # self.worker_thread.finished.connect(self.remove_worker)
            self.worker_thread.start()

    def enable_widgets(self):
        self.csv_file_textedit.setEnabled(True)
        self.get_csv_btn.setEnabled(True)
        self.export_csv_btn.setEnabled(True)

    def remove_worker(self):
        # Disconnect the signals
        self.worker.table_data.disconnect()
        self.worker.graph_data.disconnect()

        # Stop the thread
        self.worker_thread.quit()
        self.worker_thread.wait()
        self.worker_thread.exit()

        # Set the worker and thread to None
        self.worker = None
        self.worker_thread = None

    def update_table(self, orginal_text,summarized_text,sentiment_analysis_result):
        # Create a new row and insert data into the table
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        # Data to insert into each column (you can replace these with your own data)
        data1 = orginal_text
        data2 = summarized_text
        data3 = sentiment_analysis_result
        
        # Insert the data into the table
        self.result_table.setItem(row_position, 0, qtw.QTableWidgetItem(data1))
        self.result_table.setItem(row_position, 1, qtw.QTableWidgetItem(data2))
        item = qtw.QTableWidgetItem(data3)
        item.setTextAlignment(qtc.Qt.AlignCenter)
        self.result_table.setItem(row_position, 2, item)
    
    def update_graph(self,positive1,negative1,neutral1):
        # print(positive1,negative1,neutral1)
        self.positive = positive1
        self.negative = negative1
        self.neutral = neutral1

        if self.pie_chart is not None:
            # Remove the existing pie chart from the layout
            # Clear the existing figure
            # self.pie_chart.figure.clear()
            # self.pie_chart.figure.clf()
            # Close all open figures
            plt.close('all')
            self.graphLayout.removeWidget(self.pie_chart)
            if self.positive or self.negative or self.neutral:
                #create a new graph
                self.pie_chart = self.create_pie_chart()
                #add the new graph to the layout
                self.graphLayout.addWidget(self.pie_chart)
        else:
            if self.positive or self.negative or self.neutral:
                #create a new graph
                self.pie_chart = self.create_pie_chart()
                #add the new graph to the layout
                self.graphLayout.addWidget(self.pie_chart)


    def create_pie_chart(self):
        # Sample data
        self.categories = ['Positive', 'Negative', 'Neutral']
        

        self.values = [self.positive, self.negative, self.neutral]

        # Create a figure and a pie chart
        self.fig, self.ax = plt.subplots()
        self.pie = self.ax.pie(self.values, labels=self.categories, autopct=lambda p: '{:.0f}'.format(p * sum(self.values) / 100), startangle=140)
        self.ax.set_title("Sentiment Analysis Statistics")

        # Create a canvas to display the Matplotlib figure
        canvas = FigureCanvas(self.fig)
        canvas.setParent(self)

        return canvas

    def exportToCSV(self):
        file_format = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        filename = f'sentiment_analysis_result_{file_format}.csv'

        with open(filename, 'w', newline='',encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in range(self.result_table.rowCount()):
                row_data = [self.result_table.item(row, col).text() for col in range(self.result_table.columnCount())]
                csv_writer.writerow(row_data)


class WorkerThread(qtc.QObject):


    table_data = qtc.pyqtSignal(str,str,str)
    graph_data = qtc.pyqtSignal(int,int,int)

    # def __init__(self, positive1, negative1, neutral1):
    #     super(WorkerThread, self).__init__()
    #     self.positive1 = positive1
    #     self.negative1 = negative1
    #     self.neutral1 = neutral1
    def __init__(self,csv_file_path):
        super(WorkerThread, self).__init__()
        self.csv_file_path = csv_file_path
        self.positive1 = 0
        self.negative1 = 0
        self.neutral1 = 0
        # print("WorkerThread")
    def run(self):
        try:
            url = "https://nocodefunctions.com/api/sentimentForAText"
            querystring = {"text-lang":"en","text":"","explanation":"off","output-format":"json","explanation-lang":"en_US"}

            with open(self.csv_file_path, 'r',encoding="utf-8") as file:
                # Try to open the file
                csv_reader = csv.reader(file)
                
                # If the file is opened successfully, you can proceed with reading it.
                # Skip the header row if it exists
                # next(csv_reader, None)
                
                # Iterate through the rows and append the data to a list
                data = [row1[0] for row1 in csv_reader]
                for row in data:
                    # print(row)
                    # time.sleep(1)
                    original_text = row
                    summary = summarizer(original_text, max_length=130, min_length=30, do_sample=False)
                    # print(summary)
                    summarized_text = str(summary[0]["summary_text"])
                    querystring["text"] = str(original_text)
                    try:
                        response = requests.request("GET", url, params=querystring)
                        sentiment_analysis_result = response.json()
                        sentiment_analysis_result=sentiment_analysis_result["sentiment"]
                    except:
                        sentiment_analysis_result = ""
                    
                    if sentiment_analysis_result == "positive feeling":
                        self.positive1 = self.positive1 + 1
                    
                    if sentiment_analysis_result == "negative feeling":
                        self.negative1 = self.negative1 + 1
                    
                    if sentiment_analysis_result == "neutral feeling":
                        self.neutral1 = self.neutral1 + 1
                
                    # sentiment_analysis_result = ""
                    self.table_data.emit(original_text,summarized_text,sentiment_analysis_result)
                    self.graph_data.emit(self.positive1,self.negative1,self.neutral1)
                    
                # Now, 'data' contains the CSV data as a list of lists
                # Each inner list represents a row in the CSV file
                # print(data)
        except FileNotFoundError:
            print(f"The file '{self.csv_file_path}' does not exist.")
        except PermissionError:
            print(f"You don't have permission to read the file '{self.csv_file_path}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    
    







app = qtw.QApplication(sys.argv)
# Apply the complete dark theme to your Qt App.
qdarktheme.setup_theme("light")
window = Ui()
sys.exit(app.exec_())