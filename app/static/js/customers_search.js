$(document).ready(function(){
    $("#show_customers").hide();
    $(".btn_search_all").click(function(){
        $.getJSON("{{url_for('.search_customers')}}",{search:"all"},function(json, status, xhr) {
            if (json["show_windows"] == true) {
              alert(json["search_msg"]);
            }
            if (json["customers"] != null) {
              if (json["customers"].length == 0) {
                alert("暂无用户")
              } else {
                  html = "";
                  $("#show_customers").show();
                  let customer;
                  let i;
                  i=0;
                  html += "<tr> \
                            <td>身份证号</td> \
                            <td>负责员工身份证号</td> \
                            <td>姓名</td> \
                            <td>电话</td> \
                            <td>住址</td> \
                            <td></td> \
                            <td></td> \
                            <td></td> \
                            </tr>";
                  for (customer of json["customers"]) {
                    $("#customers_table").empty();
                      html += "<tr id=\"customers\">";
                      html = html + "<td>"+ customer[0] +"</td>";
                      html = html + "<td>"+ (customer[1] != null ? customer[1] : "") +"</td>";
                      html = html + "<td>"+ customer[2] +"</td>";
                      html = html + "<td>"+ customer[3] +"</td>";
                      html = html + "<td>"+ customer[4] +"</td>";
                      html = html + "<td style=\"border-color: #0be370\"> \
                          <div class=\"search\" style=\"width: 50px\"> \
                              <form style=\"margin-left: 0px\" method=\"post\" action=\"{{ url_for('.customers_show', ID=" + customer[0] + ") }}\"> \
                              <input style=\"width: 50px; background-color: rgb(63, 137, 236); color: rgb(255, 255, 255);\"  type=\"submit\" name=\"show\" value=\"查看\"> \
                          </form> \
                          </div> \
                      </td>";
                      html = html + "<td style=\"border-color: #0be370\"> \
                          <div class=\"search\" style=\"width: 50px\"> \
                              <form style=\"margin-left: 0px\" method=\"post\" action=\"{{ url_for('.customers_edit', ID=" + customer[0] + ") }}\"> \
                              <input style=\"width: 50px; background-color: rgb(63, 137, 236); color: rgb(255, 255, 255);\"   type=\"submit\" name=\"edit\" value=\"编辑\"> \
                          </form> \
                          </div> \
                      </td>";
                      html = html + "<td style=\"border-color: #0be370\"> \
                          <div class=\"search\" style=\"width: 50px\"> \
                              <form style=\"margin-left: 0px\" method=\"post\" action=\"{{ url_for('.customers_delete', ID=" + customer[0] + ") }}\"> \
                              <input style=\"width: 50px; background-color: rgb(63, 137, 236); color: rgb(255, 255, 255);\" type=\"submit\" name=\"delete\" value=\"删除\"> \
                          </form> \
                          </div> \
                      </td> \
                    </tr>";
                      html += "</tr>";
                  }
                  $("#customers_table").append(html);
              }
            }
        })
    })
  })