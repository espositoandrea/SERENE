import collect, {Collector} from "../collector";

setInterval(function () {
    collect()
        .then(data => {
            console.log(data);
        });
}, 1000);