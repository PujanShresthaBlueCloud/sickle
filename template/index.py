template = """
<html>
  <body>
    <h3>Sickle Cell Detection Report</h3>
    <table class="report">
      <tr style="text-align: left;">
        <th colspan="4">Patient Information:</th>
      </tr>
      <tr style="text-align: left;">
        <td width="20%">First name:</td>
        <td style="text-align: left;">{}</td>
        <td width="20%">Last name:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <td>Age:</td>
        <td style="text-align: left;">{}</td>
        <td>Sex:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <td>Address:</td>
        <td style="text-align: left;">{}</td>
        <td>Date of Test:</td>
        <td style="text-align: left;">{}</td>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4"></th>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4">Test Results:</th>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4"></th>
      </tr>
      <tr style="text-align: left;">
        <td colspan="4">The results of your recent laboratory tests indicate that you have sickle cell disease. Sickle cell disease is a genetic blood disorder that affects the shape of red blood cells. In people with sickle cell disease, the red blood cells are shaped like crescents or sickles instead of round discs.</td>
      </tr>
      <tr style="text-align: left;">
        <th colspan="4">Management and Treatment:</th>
      </tr>
      <tr style="text-align: left;">
        <td colspan="4">There is currently no cure for sickle cell disease, but there are treatments that can help manage symptoms and prevent complications. Treatment options include pain management, antibiotics to prevent infections, blood transfusions, and bone marrow transplants in severe cases.</td>
      </tr>
    </table>
  </body>
</html>
"""