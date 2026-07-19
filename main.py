import networkx as nx
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
metro_map = nx.Graph()
stations_line_1 = ["Каменная Горка", "Кунцевщина", "Спортивная", "Пушкинская", "Молодежная", "Фрунзенская", "Немига", "Купаловская", "Первомайская", "Пролетарская", "Тракторный завод", "Партизанская", "Автозаводская", "Могилевская"]
stations_line_2 = ["Малиновка", "Петровщина", "Михалово", "Грушевка", "Институт Культуры", "Площадь Ленина", "Октябрьская", "Площадь Победы", "Площадь Якуба Коласа", "Академия наук", "Парк Челюскинцев", "Московская", "Восток", "Борисовский тракт", "Уручье"]
stations_line_3 = ["Юбилейная площадь", "Площадь Франтишка Богушевича", "Вокзальная", "Ковальская Слобода", "Аэродромная", "Неморшанский Сад", "Слуцкий Гостинец"]
for station in stations_line_1:
    metro_map.add_node(station, line=1)
for station in stations_line_2:
    metro_map.add_node(station, line=2)
for station in stations_line_3:
    metro_map.add_node(station, line=3)
metro_map.nodes["Купаловская"]["line"] = 12
metro_map.nodes["Октябрьская"]["line"] = 12
metro_map.nodes["Площадь Ленина"]["line"] = 31
metro_map.nodes["Вокзальная"]["line"] = 31
metro_map.nodes["Фрунзенская"]["line"] = 32
metro_map.nodes["Юбилейная площадь"]["line"] = 32
edges_line_1 = [("Каменная Горка", "Кунцевщина", 2), ("Кунцевщина", "Спортивная", 3), ("Спортивная", "Пушкинская", 2), ("Пушкинская", "Молодежная", 3), ("Молодежная", "Фрунзенская", 2), ("Фрунзенская", "Немига", 2), ("Немига", "Купаловская", 2), ("Купаловская", "Первомайская", 2), ("Первомайская", "Пролетарская", 2), ("Пролетарская", "Тракторный завод", 3), ("Тракторный завод", "Партизанская", 3), ("Партизанская", "Автозаводская", 2), ("Автозаводская", "Могилевская", 3)]
edges_line_2 = [("Малиновка", "Петровщина", 3), ("Петровщина", "Михалово", 2), ("Михалово", "Грушевка", 2), ("Грушевка", "Институт Культуры", 3), ("Институт Культуры", "Площадь Ленина", 2), ("Площадь Ленина", "Октябрьская", 2), ("Октябрьская", "Площадь Победы", 2), ("Площадь Победы", "Площадь Якуба Коласа", 2), ("Площадь Якуба Коласа", "Академия наук", 2), ("Академия наук", "Парк Челюскинцев", 2), ("Парк Челюскинцев", "Московская", 2), ("Московская", "Восток", 3), ("Восток", "Борисовский тракт", 3), ("Борисовский тракт", "Уручье", 3)]
edges_line_3 = [("Юбилейная площадь", "Площадь Франтишка Богушевича", 2), ("Площадь Франтишка Богушевича", "Вокзальная", 2), ("Вокзальная", "Ковальская Слобода", 3), ("Ковальская Слобода", "Аэродромная", 2), ("Аэродромная", "Неморшанский Сад", 2), ("Неморшанский Сад", "Слуцкий Гостинец", 3)]
interchanges = [("Купаловская", "Октябрьская", 4), ("Площадь Ленина", "Вокзальная", 4), ("Фрунзенская", "Юбилейная площадь", 4)]
metro_map.add_weighted_edges_from(edges_line_1)
metro_map.add_weighted_edges_from(edges_line_2)
metro_map.add_weighted_edges_from(edges_line_3)
metro_map.add_weighted_edges_from(interchanges)
class MetroApp(App):
    def build(self):
        self.title = "Навигатор Минского Метро"
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        main_layout.add_widget(Label(text="НАВИГАТОР МИНСКОГО МЕТРО", font_size='20sp', color=(0, 0.5, 1, 1), size_hint_y=None, height=40))
        main_layout.add_widget(Label(text="Станция отправления:", font_size='14sp', size_hint_y=None, height=20))
        self.entry_start = TextInput(multiline=False, font_size='16sp', size_hint_y=None, height=45, halign='center')
        main_layout.add_widget(self.entry_start)
        main_layout.add_widget(Label(text="Станция прибытия:", font_size='14sp', size_hint_y=None, height=20))
        self.entry_end = TextInput(multiline=False, font_size='16sp', size_hint_y=None, height=45, halign='center')
        main_layout.add_widget(self.entry_end)
        btn_calc = Button(text="ПОСТРОИТЬ МАРШРУТ", font_size='16sp', bold=True, background_color=(0, 0.6, 0, 1), size_hint_y=None, height=50)
        btn_calc.bind(on_press=self.calculate_route)
        main_layout.add_widget(btn_calc)
        scroll = ScrollView()
        self.result_label = Label(text="Здесь появится ваш маршрут", font_size='14sp', color=(0.7, 0.7, 0.7, 1), halign='center', valign='top', size_hint_y=None)
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        scroll.add_widget(self.result_label)
        main_layout.add_widget(scroll)
        return main_layout
    def calculate_route(self, instance):
        start = self.entry_start.text.strip()
        end = self.entry_end.text.strip()
        if start not in metro_map or end not in metro_map:
            self.result_label.text = "[Ошибка]: Одной из станций нет в базе!\nПроверьте заглавные буквы."
            return
        try:
            shortest_path = nx.dijkstra_path(metro_map, source=start, target=end, weight='weight')
            travel_time = nx.dijkstra_path_length(metro_map, source=start, target=end, weight='weight')
            route_str = " -> \n".join(shortest_path)
            self.result_label.text = f"Оптимальный маршрут:\n{route_str}\n\nВремя в пути: {travel_time} минут(ы)."
        except Exception as e:
            self.result_label.text = "Не удалось рассчитать маршрут."
if __name__ == '__main__':
    MetroApp().run()
