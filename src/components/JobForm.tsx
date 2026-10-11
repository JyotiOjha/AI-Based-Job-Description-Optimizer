import { useState } from "react";
import { generateJD } from "../services/api";
import { useNavigate } from "react-router-dom";

const JobForm = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    title: "",
    experience: "",
    skills: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError("");

      const payload = {
        ...form,
        skills: form.skills.split(",").map((s) => s.trim()),
      };

      const res = await generateJD(payload);

      // 🔥 Navigate to result page with data
      navigate("/result", { state: res });

    } catch (err: any) {
      setError("Something went wrong!");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Create Job</h2>

      <input name="title" placeholder="Job Title" onChange={handleChange} /><br /><br />
      <input name="experience" placeholder="Experience" onChange={handleChange} /><br /><br />
      <input name="skills" placeholder="Skills (comma separated)" onChange={handleChange} /><br /><br />
      <textarea name="description" placeholder="Description" onChange={handleChange} /><br /><br />

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Generating..." : "Generate JD"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default JobForm;