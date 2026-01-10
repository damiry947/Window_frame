import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPainterPath, QPen, QLinearGradient

class RoundedWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.setWindowFlags(Qt.FramelessWindowHint)  # Убираем рамку
        self.setAttribute(Qt.WA_TranslucentBackground)  # Делаем фон прозрачным
        
        # Размеры окна
        self.window_width = 400
        self.window_height = 400
        
        # Радиус закругления
        self.corner_radius = 40
        
        # Переменные для перемещения окна
        self.dragging = False
        self.offset = QPoint()
        
        # Переменные для изменения размера
        self.resizing = False
        self.resize_edge = None
        self.min_size = 200
        self.max_size = 800
        
        # Установка размеров
        self.resize(self.window_width, self.window_height)
        
    def paintEvent(self, event):
        # Создаем QPainter для рисования
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Включаем сглаживание
        
        # Создаем путь с закругленными краями
        path = QPainterPath()
        path.addRoundedRect(0, 0, 
                           self.width(), 
                           self.height(), 
                           self.corner_radius, 
                           self.corner_radius)
        
        # Заливаем черным цветом
        painter.fillPath(path, QColor(30, 30, 30))
        
        # Рисуем блик вокруг окна
        self.draw_glow(painter)
        
        # Рисуем градиентный верхний край для красоты
        self.draw_top_gradient(painter, path)
        
    def draw_glow(self, painter):
        """Рисуем свечение вокруг окна"""
        glow_radius = 10
        glow_color = QColor(100, 150, 255, 50)  # Голубоватое свечение
        
        # Рисуем несколько контуров с разной прозрачностью для эффекта свечения
        for i in range(glow_radius, 0, -1):
            alpha = 30 - (i * 3)
            if alpha < 0:
                alpha = 0
                
            glow_path = QPainterPath()
            glow_path.addRoundedRect(-i, -i, 
                                    self.width() + i*2, 
                                    self.height() + i*2, 
                                    self.corner_radius + i, 
                                    self.corner_radius + i)
            
            painter.setPen(QPen(QColor(100, 150, 255, alpha), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(glow_path)
    
    def draw_top_gradient(self, painter, path):
        """Рисуем градиент на верхней части окна"""
        gradient = QLinearGradient(0, 0, 0, 50)
        gradient.setColorAt(0, QColor(60, 60, 60))
        gradient.setColorAt(1, QColor(30, 30, 30))
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(path)
    
    def mousePressEvent(self, event):
        # Определяем, где произошел клик
        if event.button() == Qt.LeftButton:
            # Проверяем, не кликнули ли мы в области для изменения размера
            if self.is_resize_area(event.pos()):
                self.resizing = True
                self.resize_edge = self.get_resize_edge(event.pos())
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                # Если не в области изменения размера, то перемещаем окно
                self.dragging = True
                self.offset = event.pos()
                self.setCursor(Qt.ClosedHandCursor)
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            # Перемещаем окно
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)
        elif self.resizing and self.resize_edge:
            # Изменяем размер окна
            self.resize_window(event.pos())
    
    def mouseReleaseEvent(self, event):
        # Сбрасываем флаги при отпускании кнопки мыши
        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)
    
    def resize_window(self, mouse_pos):
        """Изменяет размер окна в зависимости от границы"""
        if self.resize_edge == 'bottom_right':
            new_width = max(self.min_size, mouse_pos.x())
            new_height = max(self.min_size, mouse_pos.y())
            self.resize(new_width, new_height)
        elif self.resize_edge == 'right':
            new_width = max(self.min_size, mouse_pos.x())
            self.resize(new_width, self.height())
        elif self.resize_edge == 'bottom':
            new_height = max(self.min_size, mouse_pos.y())
            self.resize(self.width(), new_height)
        
        # Обновляем окно
        self.update()
    
    def is_resize_area(self, pos):
        """Проверяет, находится ли позиция в области для изменения размера"""
        resize_margin = 10
        
        # Проверяем правую границу
        if pos.x() > self.width() - resize_margin:
            return True
        # Проверяем нижнюю границу
        if pos.y() > self.height() - resize_margin:
            return True
        # Проверяем нижний правый угол
        if (pos.x() > self.width() - resize_margin and 
            pos.y() > self.height() - resize_margin):
            return True
        
        return False
    
    def get_resize_edge(self, pos):
        """Определяет, какую границу мы изменяем"""
        resize_margin = 10
        
        if (pos.x() > self.width() - resize_margin and 
            pos.y() > self.height() - resize_margin):
            return 'bottom_right'
        elif pos.x() > self.width() - resize_margin:
            return 'right'
        elif pos.y() > self.height() - resize_margin:
            return 'bottom'
        
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Создаем окно
    window = RoundedWindow()
    
    # Устанавливаем заголовок
    window.setWindowTitle("Rounded Window with Glow")
    
    # Показываем окно
    window.show()
    
    sys.exit(app.exec_())