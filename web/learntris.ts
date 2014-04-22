class LearntrisConsole {
    
    constructor() {
	this.game = new Phaser.Game(800, 600, Phaser.AUTO, 'content', { 
	    preload: this.preload, create: this.create });
    }
    
    game: Phaser.Game;
    blocks: number[];

    preload() {
	this.game.load.spritesheet('blocks', 'assets/blocks.png', 16, 16);
    }

    create() {
	this.blocks = new Array(8);
	var x = this.game.world.centerX - (7 * 16);
	var y = this.game.world.centerY - 8;
	for (var i = 0; i < 7; ++i) {
	    this.blocks[i] = this.game.add.sprite(x, y, 'blocks', i);
	    x += 32;
      }
    }
    
}

window.onload = () => {
    var game = new LearntrisConsole();
};
