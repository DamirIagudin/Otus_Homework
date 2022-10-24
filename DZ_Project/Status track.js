//@ts-check : enable more type checks for editor
//@handler  : Определение статуса грузовика
//@author   : Дамир

/**
 * Makes the sum of two numbers
 * @author `damirjud@gmail.com`
 */
function process(speed, massa) {
  let status = "";
  if (speed > 0){
    if (massa > 0) {
      status = "На склад";
    } else{
      status = "На ферму";
    } 
  } else {
    if (massa > 0) {
      status = "Стоянка-полный";
    } else{
      status = "Стоянка-пустой";
    }     
  }

  return { status };
}

/* ↑ here ends original handler code  */
/* ↓ here goes generated debug  code  */

/* 01. define test values */
const config = {};
const packet = {
  "speed": null,
  "massa": null
};

/* 02. run handler code */
const result = process(
  packet["speed"],
  packet["massa"]
);

/* 03. log handler results */
console.log({
  "status": result["status"]
});

