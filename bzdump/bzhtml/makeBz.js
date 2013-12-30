function makeBz() {
    var file = document.querySelector('#f').files[0];
        var fr = new FileReader();
    var pallet = (function(){
        p = new Array();
        for(r=0; r<=0xff; r+=0x33)
                for(g=0; g<=0xff; g+=0x33)
                        for(b=0; b<=0xff; b+=0x33)
                                p.push([r,g,b]);
        for(gr=0; gr<=0xff; gr+=0x11)
                p.push([gr,gr,gr]);
        p.push([0xC0,0xC0,0xC0]);
        p.push([0x80,0x80,0x80]);
        p.push([0x80,0x00,0x00]);
        p.push([0x80,0x00,0x80]);
        p.push([0x00,0x80,0x00]);
        p.push([0x00,0x80,0x80]);
        for(i=0;i<17;i++)
            p.push([0x00,0x00,0x00]);
        p.push([0xff,0xff,0xff]);
        return p;
    })();

    fr.addEventListener('load', function(e){
                var mapElement = document.querySelector('#c');
                var WIDTH = 256;
                var HEIGHT = Math.ceil(e.target.result.length / WIDTH);
                mapElement.width = WIDTH;
                mapElement.height = HEIGHT;
                var mapContext = mapElement.getContext('2d');
                var mapImage = mapContext.createImageData(WIDTH, HEIGHT);
                for (var i = 0; i < e.target.result.length; i++){
                        var bin = e.target.result[i].charCodeAt();
                        var indexed = pallet[bin];
                        mapImage.data[i * 4 + 0] = indexed[0];
                        mapImage.data[i * 4 + 1] = indexed[1];
                        mapImage.data[i * 4 + 2] = indexed[2];
                        mapImage.data[i * 4 + 3] = 255;//Alpha
                }
                mapContext.putImageData(mapImage, 0, 0);
        }, false);
    fr.readAsBinaryString(file);
}
