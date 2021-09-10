
// DATETIME PICKER

$(document).ready(function(){

    $(".dateinput").datetimepicker({timepicker: false, format:'m/d/Y', theme:'dark', changeYear: true, changeMonth: true, minDate: 0});
  
    $("#id_start_time").datetimepicker({
        format:'h:i A',
        datepicker:false,
        theme:'dark',
        step: 30,
        formatTime: 'h:ia',
        validateOnBlur: false
    });
    $("#id_end_time").datetimepicker({
        format:'h:i A',
        datepicker:false,
        theme:'dark',
        step: 30,
        formatTime: 'h:ia',
        validateOnBlur: false
    });
  
  });


// BANNER FUNCTIONALITY

const banner = document.querySelector("#bannerid");

window.addEventListener("scroll", () => {
    const banner = document.querySelector("#bannerid")
    const currentScroll = window.pageYOffset;
    if (currentScroll > 100) {
        banner.classList.add("hidden");
        console.log(currentScroll);
    }
})