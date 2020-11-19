var xl = require('xlsx');
var fs = require('fs');
const { none } = require('ramda');

// console.clear();

// var workbook = xl.readFile("D_掉落组.xlsx")

// //var dataa =xl.utils.sheet_to_json(worksheet);

// const sheetNames = workbook.SheetNames; // 返回 ['sheet1', 'sheet2']

// // 根据表名获取对应某张表

// const worksheet = workbook.Sheets[sheetNames[0]];

// var dataa =xl.utils.sheet_to_json(worksheet);

// var str = JSON.stringify(dataa);

// console.log(str)
class utils {
    constructor() {
    }
    /**
     * @desc: 获取指定sheet表的值

     * @param {workbookPath} workbookPath : 工作簿位置
     * @param {Num} Num : 第几个sheet表  0第一个 1第二个 ...
     *
     * @return {object} data: json格式sheet表数据
     */
    readSheet(workbookPath, Num) {
        var workbook = xl.readFile(workbookPath)
        // var dataa =xl.utils.sheet_to_json(SheetName);
        const sheetNames = workbook.SheetNames; // 返回 ['sheet1', 'sheet2']
        // 根据表名获取对应某张表
        const worksheet = workbook.Sheets[sheetNames[Num]];
        var data = xl.utils.sheet_to_json(worksheet);
        // var str = JSON.stringify(dataa);
        // console.log(str, dataa.length)
        // this.saveToFile("./a.json", str)
        return data
    }
    /**
     * @desc: 保存数据到文件中（同步运行）

     * @param {filePath} filePath : 文件地址
     * @param {content} content : 要保存的内容，必须是字符串。
     * @param {sync} sync : 同步还是异步执行，默认为同步, sync=false为异步执行
     * 
     * @return {object} 
     */
    saveToFile(filePath, content, sync=true) {
        if(sync){
            fs.appendFileSync(filePath, content, function (err) {
                if (err) {
                    console.log("出现错误:", err)
                    return { "sc": 0, "filePath": none, "msg": err }
                }
                return { "sc": 1, "filePath": filePath, "msg": "保存成功" }
            });
        }else{
            fs.appendFile(filePath, content, function (err) {
                if (err) {
                    console.log("出现错误:", err)
                    return { "sc": 0, "filePath": none, "msg": err }
                }
                return { "sc": 1, "filePath": filePath, "msg": "保存成功" }
            });
        }
        
    }
    

    /**
     * @desc: 生成开始值到结束值之间的随机数

     * @param {minNum} minNum : 开始值
     * @param {maxNum} maxNum : 结束值
     *
     * @return {object} int类型数字
     */
    randomNum(minNum, maxNum) {
        switch (arguments.length) {
            case 1:
                return parseInt(Math.random() * minNum + 1, 10);
                break;
            case 2:
                return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
                break;
            default:
                return 0;
                break;
        }
    }
    
    
    /**
     * @desc: 判断二维数组array中是否存在一维数组element

     * @param {array} array : 二维数组
     * @param {element} element : 要查询的一维数组
     *
     * @return {object} int类型数字
     */
    arrayHasElement(array, element) {  // 判断二维数组array中是否存在一维数组element
        for (var el of array) {
        if (el.length === element.length) {
            for (var index in el) {
            if (el[index] !== element[index]) {
                break;
            }
            if (index == (el.length - 1)) {    // 到最后一个元素都没有出现不相等，就说明这两个数组相等。
                return true;
            }
            }
        }
        }
        return false;
    }


}
module.exports = utils

// let ut = new utils()
// console.log(ut.randomNum(0, 2))
// var a = [1,2,4]
// console.log(a.indexOf(1))
// console.log(a.indexOf(2))
// console.log(a.indexOf(3))