import arcade
import random
import time
from game_object import Car, Enemy

WIDTH = 800
HEIGHT = 700
TITLE = "Car Game"

class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        self.background = arcade.load_texture("CarGame/assets/img/carreterra.jpg")  # Carga la imagen de fondo
        self.car = Car("CarGame/assets/img/car.png", 0.2, WIDTH // 2, 100)
        self.vida = 100
        self.kilometraje = 0
        self.enemies = arcade.SpriteList()
        self.is_game_over = False
        self.exit_count = 5
        self.game_over_text = "PERDISTE!!"
        self.exit_text = f"SALIENDO EN {self.exit_count}"
        self.last_mileage_increase_time = time.time()  # Guarda el tiempo de la última actualización del kilometraje
        self.new_record_text = ""
        self.show_new_record = False
        self.new_record_timer = 0
        self.background_music = arcade.load_sound("CarGame/assets/audio/tokio.mp3")
        self.play_background_music()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)  # Dibuja el fondo
        self.car.draw()
        self.enemies.draw()
        arcade.draw_text(f"Vida = {self.vida}", 10, HEIGHT - 50, arcade.color.WHITE, 20)  # Dibuja el texto de la vida
        arcade.draw_text(f"Kilometraje = {self.kilometraje}Km", 10, HEIGHT - 80, arcade.color.WHITE, 20)  # Dibuja el texto del kilometraje
        if self.is_game_over:
            arcade.draw_text(self.game_over_text, WIDTH // 2, HEIGHT // 2 + 50, arcade.color.RED, font_size=50, anchor_x="center")
            arcade.draw_text(self.exit_text, WIDTH // 2, HEIGHT // 2, arcade.color.RED, font_size=30, anchor_x="center")
        if self.show_new_record:
            arcade.draw_text(self.new_record_text, WIDTH // 2, HEIGHT // 2, arcade.color.BLACK, font_size=30, anchor_x="center")
    
    def play_background_music(self):
            arcade.play_sound(self.background_music)
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.car.change_x = -4
        elif key == arcade.key.RIGHT:
            self.car.change_x = 4

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.car.change_x = 0
    
    def on_update(self, delta_time):
        if not self.is_game_over:
            self.car.update()
            # Generar enemigos aleatoriamente
            if random.randint(0, 100) < 1:   # Controla la frecuencia de generación
                enemy = Enemy("CarGame/assets/img/bomba.png", 0.06, random.randint(0, WIDTH), HEIGHT)
                self.enemies.append(enemy)
            
            # Restringir el movimiento del auto por las paredes
            if self.car.left < 0:
                self.car.left = 0
            if self.car.right > WIDTH:
                self.car.right = WIDTH
                
            for enemy in self.enemies:
                enemy.center_y -= enemy.speed  # Mover hacia abajo
                
                # Colisión entre enemigos y auto
                if arcade.check_for_collision(self.car, enemy):
                    self.vida -= enemy.damage
                    enemy.remove_from_sprite_lists()

            # Eliminar enemigos que hayan caído fuera de la pantalla
            for enemy in self.enemies:
                if enemy.bottom < 0:
                    enemy.remove_from_sprite_lists()
            
            # Incrementar el kilometraje cada 5 segundos
            current_time = time.time()
            if current_time - self.last_mileage_increase_time >= 5:
                self.kilometraje += 10
                self.last_mileage_increase_time = current_time
                if self.kilometraje >= 100 and self.kilometraje % 100 == 0:
                    self.show_new_record = True
                    self.new_record_text = "NUEVO RÉCORD"
                    self.new_record_timer = current_time

            if self.show_new_record and current_time - self.new_record_timer >= 1:
                self.show_new_record = False
                self.new_record_text = ""

            if self.vida <= 0:
                self.is_game_over = True
            
        elif self.exit_count > 0:
            self.exit_text = f"SALIENDO EN {self.exit_count}"
            self.exit_count -= 1
            if self.exit_count == 0:
                time.sleep(5)
        else:
            arcade.close_window()
            
    def on_exit(self):
        arcade.stop_sound(self.background_music)
        super().on_exit()
        
def main():
    app = App()
    arcade.run()

if __name__ == "__main__":
    main()
