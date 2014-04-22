var gap = 1;
var csize = 16;
var gridw = 10;
var gridh = 22;

function randcolor() : number {
    return Math.floor(Math.random() * 7);
}

class LearntrisConsole {


    constructor() {
	this.game = new Phaser.Game(800, 600, Phaser.AUTO, 'content', {
	    preload: this.preload,
	    create: this.create,
	    update: this.update,
	});
    }

    game: Phaser.Game;
    blocks: Phaser.Sprite[][];

    preload() {
	this.game.load.spritesheet('blocks', 'assets/blocks.png', 16, 16);
    }

    create() {
	this.blocks = new Array(gridh);
	var y = this.game.world.centerY - (gridh/2 * (csize+gap));
	for (var j = 0; j < gridh; ++j) {
	    this.blocks[j] = new Array(gridw);
	    var x = this.game.world.centerX - (gridw/2 * (csize+gap));
	    for (var i = 0; i < gridw; ++i) {
		this.blocks[j][i]
		    = this.game.add.sprite(x, y, 'blocks', randcolor());
		x += csize + gap;
	    }
	    y += csize + gap;
	}
    }

    update() {
	for (var j = 0; j < gridh; ++j) for (var i = 0; i < gridw; ++i) {
	    var block = this.blocks[j][i];
	    block.frame = randcolor();
	}
    }

}

window.onload = () => {
    var game = new LearntrisConsole();
};
