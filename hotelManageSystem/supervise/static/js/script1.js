document.addEventListener('DOMContentLoaded', function () {
    const Mdec = document.querySelector('.Mtdec-btn');
    const Minc = document.querySelector('.Mtinc-btn');
    const mdec = document.querySelector('.mtdec-btn');
    const minc = document.querySelector('.mtinc-btn');
    const M = document.querySelector('.Mtemp');
    const m = document.querySelector('.mtemp');
    const modeButtons = document.querySelectorAll('.mode-demo');
    const w = document.querySelectorAll('.w');
    const room = document.querySelectorAll('.r');
    const sw = document.querySelectorAll('.room-turn');
    const mode = document.querySelectorAll('.mode');
    const turn = document.querySelector('.turn');
    const content = document.querySelector('#content');
    const costInput = document.getElementById('cost');  // 获取费率输入框 
    let Mtemp = 36;
    let mtemp = 16;
    let status = 0;
    let currentMode = 'cold';
    let statues = []; // 空调开关状态的数组，初始化为空数组
    let wind_l = [];
    let mode_l = [];
    function NEW(){
        for (let i = 0; i < 5; i++) {
            speedLevel = wind_l[i];
            updateIndicators(speedLevel, i);
        }     
    }
    let col = "";
    let gre = "";
    // 页面加载时获取数据
    fetch('/acmanage/get-center-aircondition/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                Mtemp = data.centralaircondition.Max_temperature;
                mtemp = data.centralaircondition.Min_temperature;
                // 更新页面显示的温度
                M.textContent = Mtemp;
                m.textContent = mtemp;
                status = data.centralaircondition.airCondition_status;
                statues = data.air_conditions.map(ac => ac.air_condition_status);
                wind_l = data.air_conditions.map(ac => ac.speed);  // 获取风速
                mode_l = data.air_conditions.map(ac => ac.mode);   // 获取模式 
                const cMode = data.centralaircondition.mode;
                if (cMode) {
                    // 更新当前模式
                    updateModeButtons(cMode);
                }
                if(cMode === "cold"){
                    col = "../static/images/雪花 (1).png";
                    gre = "../static/images/雪花.png";
                }
                else{
                    col = "../static/images/太阳 (1).png";
                    gre = "../static/images/太阳.png";
                }
                update();  // 更新页面状态
            } else {
                console.error('获取数据失败:', data.message);
            }
            NEW();
            update();
            // alert(wind_l);
            // alert(mode_l);
        })
        .catch(error => {
            console.error('请求错误:', error);
        });

    
        // 更新模式按钮状态
    function updateModeButtons(cMode) {
    // 遍历所有模式按钮
        modeButtons.forEach(btn => {
            const modeValue = btn.getAttribute('data-mode');

        // 如果按钮的模式与当前模式匹配，设置为选中状态
            if (modeValue === cMode) {
                btn.style.backgroundImage = `url('${modeImages[modeValue].color}')`;  // 设置为选中模式的背景图
            } else {
                btn.style.backgroundImage = `url('${modeImages[modeValue].grayscale}')`;  // 设置为未选中模式的背景图
            }
        });

    // 更新当前选中的模式
        currentMode = cMode;
    }

    turn.addEventListener('click', function () {
        status = !status;
        sendDataToBackend();
        turn_on();


    });

    Mdec.addEventListener('click', function () {
        if (!status && Mtemp > mtemp) {
            Mtemp--;
            sendDataToBackend();
            M.textContent = Mtemp;
        }
    });

    Minc.addEventListener('click', function () {
        if (!status && Mtemp < 36) {
            Mtemp++;
            sendDataToBackend();
            M.textContent = Mtemp;
        }
    });

    mdec.addEventListener('click', function () {
        if (!status && mtemp > 16) {
            mtemp--;
            sendDataToBackend();
            m.textContent = mtemp;
        }
    });

    minc.addEventListener('click', function () {
        if (!status && mtemp < Mtemp) {
            mtemp++;
            sendDataToBackend();
            m.textContent = mtemp;
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

    


    modeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const modeValue = this.getAttribute('data-mode');
            if (!status) {
                if (currentMode === modeValue) {
                    return;
                }
                currentMode = modeValue;
                sendDataToBackend();
                modeButtons.forEach(btn => {
                    // 如果当前按钮是选中的按钮
                    if (btn === this) {
                        // 切换为选中的背景图
                        btn.style.backgroundImage = `url('${modeImages[modeValue].color}')`;
                    } else {
                        // 其他按钮恢复为未选中的背景图
                        btn.style.backgroundImage = `url('${modeImages[btn.getAttribute('data-mode')].grayscale}')`;
                    }
                });
            }
        });
    });
    function update() {
        if (status) {
            content.style.backgroundColor = '#F5F5F5';
            turn.style.backgroundImage = `url('../static/images/开.png')`
            turn.style.backgroundColor = '#4aeeed';
            document.getElementById('cost').setAttribute('readonly', '');
            let i = 0;
            room.forEach(element => {
                if(statues[i]){
                    element.style.backgroundColor = 'white';
                    element.style.borderColor = 'black';
                }else{
                    element.style.backgroundColor = '#005996';
                    element.style.borderColor = 'grey';
                }
                i++;
            });
            i = 0;
            mode.forEach(element => {
                if(statues[i]){
                    element.style.backgroundColor = 'white';
                    element.style.backgroundImage = `url('${col}')`
                }
                else{
                    element.style.backgroundColor = '#005996';
                    element.style.backgroundImage = `url('${gre}')`
                }
                i++;
            });
            i = 0;
            sw.forEach(element => {
                if(statues[i]){
                    element.style.backgroundImage = `url('../static/images/开.png')`
                    element.style.backgroundColor = '#4aeeed';
                }else{
                    element.style.backgroundImage = `url('../static/images/关.png')`
                    element.style.backgroundColor = 'red';
                }
                i++;
            });

        } else {
            content.style.backgroundColor = '#000000';
            turn.style.backgroundImage = `url('../static/images/关.png')`
            turn.style.backgroundColor = 'red';
            document.getElementById('cost').removeAttribute('readonly');
            room.forEach(element => {
                element.style.backgroundColor = '#005996';
                element.style.borderColor = 'grey';
            });
            mode.forEach(element => {
                    element.style.backgroundColor = '#005996';
                    element.style.backgroundImage = `url('${gre}')`
            });
            sw.forEach(element => {
                element.style.backgroundImage = `url('../static/images/关.png')`
                element.style.backgroundColor = 'red';
            });
        }  
    }

    function updateIndicators(speedLevel, i) {
        switch (speedLevel) {
            case 1:
                // 低风速: 只有第一个指示器变为深色
                w[i * 3].style.backgroundColor = '#575757';
                w[i * 3 + 1].style.backgroundColor = '#D6D6D6';
                w[i * 3 + 2].style.backgroundColor = '#D6D6D6';
                document.getElementById('speed-level').textContent = '1';
                break;
            case 2:
                // 中风速: 前两个指示器变为深色
                w[i * 3].style.backgroundColor = '#575757';
                w[i * 3 + 1].style.backgroundColor = '#575757';
                w[i * 3 + 2].style.backgroundColor = '#D6D6D6';
                document.getElementById('speed-level').textContent = '2';
                break;
            case 3:
                // 高风速: 所有指示器都变为深色
                w[i * 3].style.backgroundColor = '#575757';
                w[i * 3 + 1].style.backgroundColor = '#575757';
                w[i * 3 + 2].style.backgroundColor = '#575757';
                document.getElementById('speed-level').textContent = '3';
                break;
            default:
                break;
        }
    }
    
    function turn_on(){
        fetch('/acmanage/get-center-aircondition/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statues = data.air_conditions.map(ac => ac.air_condition_status);
                mode_l = data.air_conditions.map(ac => ac.mode);   // 获取模式 
                const cMode = data.centralaircondition.mode;
                if (cMode) {
                    // 更新当前模式
                    updateModeButtons(cMode);
                }
                if(cMode === "cold"){
                    col = "../static/images/雪花 (1).png";
                    gre = "../static/images/雪花.png";
                }
                else{
                    col = "../static/images/太阳 (1).png";
                    gre = "../static/images/太阳.png";
                }
                update();
            } else {
                console.error('获取数据失败:', data.message);
            }
        })
        .catch(error => {
            console.error('请求错误:', error);
        });

    }

    function update_speed(){
        fetch('/acmanage/get-center-aircondition/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statues = data.air_conditions.map(ac => ac.air_condition_status);
                wind_l = data.air_conditions.map(ac => ac.speed);  // 获取风速
                update();  // 更新页面状态
            } else {
                console.error('获取数据失败:', data.message);
            }
            NEW();
            update();
        })
        .catch(error => {
            console.error('请求错误:', error);
        });

    }


    function sendDataToBackend() {
        const rate = parseFloat(costInput.value) || 1;  // 获取费率（默认为1）
        const requestData = {
            Max_temperature: Mtemp,
            Min_temperature: mtemp,
            airCondition_status: status ? 1 : 0,  // 1表示开，0表示关
            mode: currentMode,  // 空调模式
            cost_rate: rate  // 添加费率字段
        };

        console.log('发送给后端的数据:', requestData);

        // 发送 POST 请求到后端
        fetch('/acmanage/update-center-aircondition/', {
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
                    updatePageData(data.centralaircondition);  // 更新页面上的数据
                } else {
                    console.error('同步失败:', data.message);
                }
            })
            .catch(error => {
                console.error('请求错误:', error);  // 捕获并打印错误
            });
        
        alert(status);
    }

    function updatePageData(centralAirCondition) {
        const maxTemp = centralAirCondition.Max_temperature;
        const minTemp = centralAirCondition.Min_temperature;

        // 更新页面中的温度显示
        M.textContent = maxTemp;
        m.textContent = minTemp;

        console.log('页面数据已更新:', centralAirCondition);
    }
     function updateData() {
        fetch('/acmanage/', {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            data.airList.forEach((air, index) => {
                const roomElement = document.querySelector(`.s${index + 1}`);
                if (roomElement) {
                    roomElement.querySelector('.cur-c').textContent = `当前：${air.one_time_price}￥`;
                    roomElement.querySelector('.tot-c').textContent = `累计：${air.total_price}￥`;
                    roomElement.querySelector('.set-t').textContent = `目标：${air.target_temperature}℃`;
                    roomElement.querySelector('.cur-t').textContent = `当前：${air.current_temperature}℃`;

                }
            });
    
           
        })
        .catch(error => console.error('Error fetching data:', error));
    }
    

    // 初次获取数据
    updateData();

    //每5秒更新一次数据
    setInterval(updateData,500);
    setInterval(update_speed,500);
});