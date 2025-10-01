from flask import Flask, jsonify, request
app = Flask(__name__)

employees = [
    {"id":1,"name":"Matti Meikäläinen","status":"new"},
    {"id":2,"name":"Maija Mallikas","status":"new"}
]

@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):
    data = request.json
    for e in employees:
        if e["id"] == id:
            e.update(data)
            return jsonify(e)
    return jsonify({"error":"not found"}),404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
