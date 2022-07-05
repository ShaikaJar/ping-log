function replace_arg(arg_name, new_value) {
    src_str = image.src
    start = src_str
    if (start.includes(arg_name + '=')) {
        start = src_str.split(arg_name + '=')[0] + arg_name + '='
    } else {
        image.src = src_str + '&' + arg_name + '=' + new_value;
        return
    }
    end = src_str.split(arg_name + '=')[1]
    if (end.includes('&')) {
        end = '&' + end.split('&')[1]
    } else {
        end = ''
    }
    image.src = start + new_value + end;
}

function rename_demo(hours){
    console.log('Ranem')
    if (hours <= 24) {
        demo.innerHTML = hours + ' Stunden';
    } else {
        days = Math.floor(hours / 24)
        demo.innerHTML = days + ' Tage';
    }
}

demo = document.getElementById('demo')
range = document.getElementById('myRange')
image = document.getElementById('refresh')


image.onload = function () {
    setTimeout(
        function () {
            replace_arg('time', (new Date().getTime()))
        },
        30 * 1000
    )
}

range.onmouseup = function () {
    range.value = Math.round(range.value)
    hours = range.value
    rename_demo(hours)
    replace_arg('max_minutes_ago', 60 * hours)
    for (let i = 0; i < 5; i++) {
        setTimeout(
            function () {
                replace_arg('time', (new Date().getTime()))
            },
            i * 2500
        )
    }
}

range.oninput = function () {
    range.value = Math.round(range.value)
    rename_demo(range.value)
}


rename_demo(range.value)

