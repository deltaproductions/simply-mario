import pytmx

import config
from platforms import Floor, FloorBottom, LeftSide, RightSide, Sky, Other


class Map:  # Карта
    def __init__(self, name):
        self.map = pytmx.load_pygame(f"data/maps/{name}.tmx")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.blocks = []
        self.create_map()

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def create_map(self):
        """
        При запуске игры карта будет создаваться ОДИН раз. На основе map_1.tmx будут создаваться блоки,
        которые затем в игре и будут обрисовываться - у каждого блока будет свойство rect нужный
        для хранения координат, вычисления столкновений с игроком, а так же свойство image нужное для хранения
        изображения блока и для его дальнейшей отрисовки (отрисовка по координатам rect).
        О самих блоках читай в файле platforms.py
        :return:
        """
        for y in range(self.height):
            blocks_row = []
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)

                if self.get_tile_id((x, y)) in [205, 206, 71, 72]:
                    new_block = Floor(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image)
                elif self.get_tile_id((x, y)) in [105, 106]:
                    new_block = FloorBottom(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image)
                elif self.get_tile_id((x, y)) in [72, 106]:
                    new_block = RightSide(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image
                    )
                elif self.get_tile_id((x, y)) in [71, 105]:
                    new_block = LeftSide(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image
                    )
                elif self.get_tile_id((x, y)) in []:
                    new_block = Sky(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image)
                else:
                    new_block = Other(
                        x * config.TILE_SIZE,
                        y * config.TILE_SIZE,
                        config.TILE_SIZE,
                        config.TILE_SIZE,
                        image)

                blocks_row.append(new_block)
            self.blocks.append(blocks_row)
