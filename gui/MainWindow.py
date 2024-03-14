from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QMainWindow,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
    QCheckBox,
    QLabel,
    QMessageBox,
    QProgressBar
)
from core.template.template import *
from core.strategies.strategies import *
from core.crossings.crossing import *
from core.inversion.inversion import *
from core.mutations.mutation import mutation
from database.DbController import DbController
from plots.plotting import plot_column
import time, asyncio


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.database = DbController()
        self.setWindowTitle("Genetic algorithm for Michalewicz function")
        self.setFixedHeight(600)
        self.setFixedWidth(350)
        np.set_printoptions(suppress = True)
        layout = QVBoxLayout()

        self.begin_txt = QLineEdit(placeholderText="Begin of the range - a")
        self.end_txt = QLineEdit(placeholderText="End of the range - b")

        self.population_amount_txt = QLineEdit(placeholderText="Population amount")
        self.epoch_amount_txt = QLineEdit(placeholderText="Amount of epochs")
        self.precision_txt = QLineEdit(placeholderText="Precision")
        self.chromosome_amount_txt = QLineEdit(
            placeholderText="Selection chromosome amount"
        )
        self.elite_strategy_amount_txt = QLineEdit(
            placeholderText="Elite strategy amount"
        )
        self.crossing_probability_txt = QLineEdit(
            placeholderText="Crossing probability"
        )
        self.mutation_probability_txt = QLineEdit(
            placeholderText="Mutation probability"
        )
        self.inversion_probability_txt = QLineEdit(
            placeholderText="Inversion probability"
        )

        self.amount_of_contestanst_txt = QLineEdit(
            placeholderText="Amount of contestants"
        )
        self.amount_of_contestanst_txt.setVisible(0)

        selection_method_label = QLabel("Selection method:")
        self.selection_method_combo = QComboBox()
        self.selection_method_combo.currentIndexChanged.connect(self.show_details)
        self.selection_method_combo.addItem("BEST")
        self.selection_method_combo.addItem("TOURNAMENT")
        self.selection_method_combo.addItem("ROULETTE")

        crossing_method_label = QLabel("Crossing method:")
        self.crossing_method_combo = QComboBox()
        self.crossing_method_combo.addItem("ONE_POINT")
        self.crossing_method_combo.addItem("TWO_POINTS")
        self.crossing_method_combo.addItem("HOMO")

        mutation_method_label = QLabel("Mutation method:")
        self.mutation_method_combo = QComboBox()
        self.mutation_method_combo.addItem("ONE_POINT")
        self.mutation_method_combo.addItem("TWO_POINTS")

        self.maximization_checkbox = QCheckBox("Maximization")

        btn_confirm = QPushButton("Confirm")
        btn_confirm.pressed.connect(self.simulate)
        
        self.progress_bar = QProgressBar(self)
        self.progress_value = 0
        
        self.begin_txt.setText("0")
        self.end_txt.setText("3.141592653589793")
        self.population_amount_txt.setText("1000")
        self.epoch_amount_txt.setText("100")
        self.precision_txt.setText("10")
        self.chromosome_amount_txt.setText("25")
        self.elite_strategy_amount_txt.setText("3")
        self.crossing_probability_txt.setText("0.8")
        self.mutation_probability_txt.setText("0.3")
        self.inversion_probability_txt.setText("0.1")
        
        layout.addWidget(self.begin_txt)
        layout.addWidget(self.end_txt)
        layout.addWidget(self.population_amount_txt)
        layout.addWidget(self.epoch_amount_txt)
        layout.addWidget(self.precision_txt)
        layout.addWidget(self.chromosome_amount_txt)
        layout.addWidget(self.elite_strategy_amount_txt)
        layout.addWidget(self.crossing_probability_txt)
        layout.addWidget(self.mutation_probability_txt)
        layout.addWidget(self.inversion_probability_txt)
        layout.addWidget(selection_method_label)
        layout.addWidget(self.selection_method_combo)
        layout.addWidget(self.amount_of_contestanst_txt)
        layout.addWidget(crossing_method_label)
        layout.addWidget(self.crossing_method_combo)
        layout.addWidget(mutation_method_label)
        layout.addWidget(self.mutation_method_combo)
        layout.addWidget(self.maximization_checkbox)
        layout.addWidget(self.progress_bar)
        layout.addWidget(btn_confirm)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_details(self, ind: int):
        self.amount_of_contestanst_txt.setVisible(0)
        if ind == 1:
            self.amount_of_contestanst_txt.setVisible(1)

    def reset(self):
        self.progress_value = 0
        self.progress_bar.reset()
        
    def update(self, value, max_value):
        if self.progress_value + value >= max_value:
            self.progress_bar.setValue(max_value)
        else:
            self.progress_value += value
            self.progress_bar.setValue(self.progress_value)

    async def calculate_result(self):
        begin = np.float64(self.begin_txt.text())
        end = np.float64(self.end_txt.text())
        precision = np.uint64(self.precision_txt.text())
        size_of_population = int(self.population_amount_txt.text())
        selection_amount = int(self.chromosome_amount_txt.text())
        epochs = int(self.epoch_amount_txt.text())
        amount_of_best = int(self.elite_strategy_amount_txt.text())
        maximization = self.maximization_checkbox.isChecked()
        
        cross_probability = float(self.crossing_probability_txt.text())
        mutation_probability = float(self.mutation_probability_txt.text())
        inversion_probability = float(self.inversion_probability_txt.text())

        info = ChromosomeInfo(begin, end, precision)
        experiment = Experiment(size_of_population, info)
        
        self.progress_bar.setRange(0, epochs)
        percent_value = epochs // 100

        homogeneous = False
        match self.crossing_method_combo.currentIndex():
            case 0:
                cross_function = onePointCrossing
            case 1:
                cross_function = twoPointCrossing
            case 2:
                cross_function = homogeneousCrossing
                homogeneous = True
            
        
        tournament = False
        
        match self.selection_method_combo.currentIndex():
            case 0:
                select_method = best_selection
            case 1:
                select_method = tournament_selection
                contestants = int(self.amount_of_contestanst_txt.text())
                tournament = True
            case 2:
                select_method = roulette_wheel
        
        mutation_points = self.mutation_method_combo.currentIndex() + 1
        
        self.database.clear_data()
        start = time.process_time()
        self.reset()
        for current_epoch in range(epochs):
            self.database.insert_values(*experiment.get_db_data(maximization))
            experiment.save_best_people(amount_of_best, maximization)
            if tournament:
                experiment.selection(select_method,selection_amount,maximization, contestants=contestants)
            else:
                experiment.selection(select_method,selection_amount,maximization)
            
            if homogeneous:
                experiment.cross(cross_function, cross_probability, homogeneous=homogeneous)
            else:    
                experiment.cross(cross_function, cross_probability)
            experiment.mutate(mutation, mutation_probability, mutation_points)
            experiment.inverse(inversion, inversion_probability)
            experiment.population.add_people(experiment.best_people)
            if not current_epoch % percent_value: 
                self.update(percent_value, epochs)

        stop = time.process_time()
        
        self.database.insert_values(*experiment.get_db_data(maximization))
        
        plot_column(self.database,1)
        plot_column(self.database,2)
        plot_column(self.database,3)
        
        result = experiment.get_result(maximization)
        point = (result.chromosomes[0].to_number(), result.chromosomes[1].to_number())
        success_info = QMessageBox()
        success_info.setText(
            f"Znaleziono rozwiązanie w {stop - start} sekund. Ma ono współrzedne {point} i wynosi {result.value}"
        )
        success_info.exec()
        
    def simulate(self):
        asyncio.run(self.calculate_result())