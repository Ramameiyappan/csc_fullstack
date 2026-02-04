import { useState } from "react";
import api from "../api/axios";
import "../styles/form.css";

const DynamicForm = ({ service, onClose }) => {
  const [data, setData] = useState({ iscsc: false });
  const [errors, setErrors] = useState({});

  const submit = async (e) => {
    e.preventDefault();

    try {
      await api.post(service.endpoint, data);
      alert("Service added successfully");
      onClose();
    } catch (error) {
      if (error.response?.data) {
        setErrors(error.response.data);

        const messages = Object.values(error.response.data)
          .flat()
          .join("\n");

        alert(messages);
      } else {
        alert("Server not reachable");
      }
    }
  };

  const handleChange = (name, value) => {
    setData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <form onSubmit={submit} className="work-form">
      <h3>{service.name}</h3>

      {service.fields.map((f) => {
        if (f.type === "select") {
          return (
            <div key={f.name}>
              <select
                value={data[f.name] || ""}
                onChange={(e) =>
                  handleChange(f.name, e.target.value)
                }
                required
              >
                <option value="">
                  Select {f.label}
                </option>

                {f.options.map((o) => (
                  <option key={o} value={o}>
                    {o}
                  </option>
                ))}
              </select>

              {errors[f.name] && (
                <p className="error">
                  {errors[f.name][0]}
                </p>
              )}
            </div>
          );
        }

        if (f.type === "checkbox") {
          return (
            <label key={f.name} className="checkbox">
              <input
                type="checkbox"
                checked={data[f.name] || false}
                onChange={(e) =>
                  handleChange(
                    f.name,
                    e.target.checked
                  )
                }
              />
              {f.label}
            </label>
          );
        }

        return (
          <div key={f.name}>
            <input
              type={f.type || "text"}
              placeholder={f.label}
              value={data[f.name] || ""}
              onChange={(e) =>
                handleChange(f.name, e.target.value)
              }
              required
            />

            {errors[f.name] && (
              <p className="error">
                {errors[f.name][0]}
              </p>
            )}
          </div>
        );
      })}

      <button type="submit">Submit</button>
    </form>
  );
};

export default DynamicForm;
