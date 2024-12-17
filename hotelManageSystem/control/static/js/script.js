document.addEventListener('DOMContentLoaded', function () {
    const decreaseBtn = document.querySelector('.decrease-btn');
    const increaseBtn = document.querySelector('.increase-btn');
    const tdec = document.querySelector('.tdecrease-btn');
    const tinc = document.querySelector('.tincrease-btn');
    const set = document.querySelector('.set');
    const indicators = document.querySelectorAll('.indicator');
    const modeButtons = document.querySelectorAll('.mode-demo');
    const turn = document.querySelector('.turn');
    const content = document.querySelector('#content');
    const c = document.querySelectorAll('.c');
    let change =0;
    let cen_status=0;
    let max_temp=36;
    let min_temp=16;
    const wind = {
        '低风速': 1,
        '中风速': 2,
        '高风速': 3
    };
    let currentTemp = 30;
    let speedLevel = wind[document.getElementById('speed-level').textContent];
    let temp = set.textContent.slice(-3, -1);
    let status = 1;
    let currentMode = document.querySelector('.empty').textContent;

    fetch('/control/get-air-condition/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                currentTemp = data.air_record.airCondition_current_temp;
                status = data.air_record.airCondition_status;
                cen_status = data.air_record.central_aircondition;
                max_temp = data.air_record.max_temp;
                min_temp = data.air_record.min_temp;
                const currentMode = data.air_record.mode;
                update();  // 更新页面状态
            } else {
                console.error('获取数据失败:', data.message);
            }
            update();
        })
        .catch(error => {
            console.error('请求错误:', error);
        });

    turn.addEventListener('click', function () {
        status = !status;
        change=1;
        if(!status){
            if(currentMode!='sun'){
                temp = 25;
                speedLevel =2;
            }
            else{
                temp = 22;
                speedLevel =2;
            }

        }
        update();
        sendDataToBackend();
        updateIndicators();
        update_data();
    });

    tdec.addEventListener('click', function () {
        if (status && temp > min_temp) {
            temp--;
            change=2;
            sendDataToBackend();
            updatetemp();
        }
    });

    tinc.addEventListener('click', function () {
        if (status && temp < max_temp) {
            temp++;
            change=2;
            sendDataToBackend();
            updatetemp();
        }
    });

    const modeImages = {
        'sun': {
            'grayscale': '../static/images/太阳.png',
            'color': '../static/images/太阳 (1).png'
        },
        'cold': {
            'grayscale': '../static/images/雪花.png',
            'color': '../static/images/雪花 (1).png'
        },
        'dry': {
            'grayscale': '../static/images/除湿.png',
            'color': '../static/images/除湿 (1).png'
        },
        'wind': {
            'grayscale': '../static/images/送风.png',
            'color': '../static/images/送风 (1).png'
        }
    };

    // 只显示当前模式
    function updateModeDisplay() {
        // 将所有模式按钮设置为灰色
        modeButtons.forEach(btn => {
            btn.style.backgroundImage = `url('${modeImages[btn.getAttribute('data-mode')].grayscale}')`;
        });

        // 将当前模式按钮设置为彩色
        document.querySelector(`[data-mode="${currentMode}"]`).style.backgroundImage = `url('${modeImages[currentMode].color}')`;
    }

    // 初始化模式显示
    updateModeDisplay();

    decreaseBtn.addEventListener('click', function () {
        if (status && speedLevel > 1) {
            speedLevel--;
            change=3;
            sendDataToBackend();
            updateIndicators();
        }
    });

    increaseBtn.addEventListener('click', function () {
        if (status && speedLevel < 3) {
            speedLevel++;
            change=3;
            sendDataToBackend();
            updateIndicators();
        }
    });

    function update() {
        if (status && cen_status) {
            content.style.backgroundColor = '#F5F5F5';
            turn.style.backgroundImage = `url('../static/images/开.png')`
            turn.style.backgroundColor = '#4aeeed';
            c.forEach(element => {
                element.style.backgroundColor = 'white';
            });
            modeButtons.forEach(element => {
                element.style.backgroundColor = 'white';
            });

        } else {
            content.style.backgroundColor = '#000000';
            turn.style.backgroundImage = `url('../static/images/关.png')`
            turn.style.backgroundColor = 'red';
            c.forEach(element => {
                element.style.backgroundColor = 'grey';
            });
            modeButtons.forEach(element => {
                element.style.backgroundColor = 'grey';
            });
        }
    }

    function updatetemp() {
        set.textContent = "目标：" + temp + "℃";
    }

    function updateIndicators() {
        switch (speedLevel) {
            case 1:
                indicators[0].style.backgroundColor = '#575757';
                indicators[1].style.backgroundColor = '#D6D6D6';
                indicators[2].style.backgroundColor = '#D6D6D6';
                document.getElementById('speed-level').textContent = '低风速';
                break;
            case 2:
                indicators[0].style.backgroundColor = '#575757';
                indicators[1].style.backgroundColor = '#575757';
                indicators[2].style.backgroundColor = '#D6D6D6';
                document.getElementById('speed-level').textContent = '中风速';
                break;
            case 3:
                indicators[0].style.backgroundColor = '#575757';
                indicators[1].style.backgroundColor = '#575757';
                indicators[2].style.backgroundColor = '#575757';
                document.getElementById('speed-level').textContent = '高风速';
                break;
        }
    }

    function sendDataToBackend() {
        const requestData = {
            current_temperature: currentTemp,
            target_temperature: temp,
            current_speed: speedLevel,
            airCondition_status: status ? 1 : 0,  // 1表示开，0表示关
            // airCondition_mode: currentMode,  // 空调模式
            service_type: change,  // 这里设置为手动模式
        };

        console.log('发送给后端的数据:', requestData);

        // 发送 POST 请求到后端
        fetch('/control/update-air-condition/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // 请求头设置为 JSON 格式
            },
            body: JSON.stringify(requestData)  // 请求体包含 JSON 数据
        })
            .then(response => response.json())  // 解析返回的 JSON 数据
            .then(data => {
                if (data.status === 'success') {
                    console.log('空调设置已同步');
                    console.log('从后端接收到的数据:', data);
                    const TempElement = document.querySelector('.set');
                    TempElement.textContent = `目标: ${data.air_record.target_temperature}℃`;
                    // updatePageData(data.air_record);  // 更新页面上的数据
                } else {
                    console.error('同步失败:', data.message);
                }
            })
            .catch(error => {
                console.error('请求错误:', error);  // 捕获并打印错误
            });
    }



    function update_data(){
        fetch('/control/get-air-condition/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                cen_status = data.air_record.central_aircondition;
                status = data.air_record.airCondition_status;
                max_temp = data.air_record.max_temp;
                min_temp = data.air_record.min_temp;
                currentTemp = data.air_record.airCondition_current_temp;
                const currentTempElement = document.querySelector('.now');
                currentTempElement.textContent = `当前: ${data.air_record.airCondition_current_temp}℃`;
                const TotaCostElement = document.querySelector('.tot.n');
                if(TotaCostElement){
                    TotaCostElement.textContent = `${data.air_record.airCondition_bill}`;
                }
                currentMode = data.air_record.airCondition_mode;
                const TempCostElement = document.querySelector('.cur.n');
                TempCostElement.textContent = ` ${data.air_record.airCondition_current_bill}`;

                update();  // 更新页面状态
                updateModeDisplay();
            } else {
                console.error('获取数据失败:', data.message);
            }
            update();
        })
        .catch(error => {
            console.error('请求错误:', error);
        });

    }

    update();
    updateIndicators();
    updatetemp();
    setInterval(update_data,500);
});
