console.log("Desk Js Loaded")

// F2 - Install, Boot & Session Hooks
// extend_bootinfo:
$(document).ready(function () {
    $(".navbar").append(
        `<span style="margin-left: 10px;">
            ${frappe.boot.quickfix_shop_name}
        </span>`
    );
});