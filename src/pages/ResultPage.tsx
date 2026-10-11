import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import { rescoreJD, getSkillGap } from "../services/api";

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state;

  // ✅ Hooks at top
  const [jd, setJd] = useState(result?.generated_jd || {});
  const [score, setScore] = useState(result?.jd_score || {});
  const [skillGap, setSkillGap] = useState<any>(null);

  const [loadingScore, setLoadingScore] = useState(false);
  const [loadingGap, setLoadingGap] = useState(false);

  // ❗ No data case
  if (!result) {
    return (
      <div style={{ padding: "20px" }}>
        <h2>No Data Found</h2>
        <button onClick={() => navigate("/")}>Go Back</button>
      </div>
    );
  }

  // 🔹 Update single field
  const updateField = (field: string, value: any) => {
    setJd({ ...jd, [field]: value });
  };

  // 🔹 Update list
  const updateList = (field: string, index: number, value: string) => {
    const updatedList = [...(jd[field] || [])];
    updatedList[index] = value;
    setJd({ ...jd, [field]: updatedList });
  };

  // 🔹 Score color
  const getScoreColor = (val: number) => {
    if (val >= 80) return "green";
    if (val >= 60) return "orange";
    return "red";
  };

  // 🔥 Re-score
  const handleRescore = async () => {
    try {
      setLoadingScore(true);
      const response = await rescoreJD(jd);
      setScore(response);
    } catch (err) {
      console.error(err);
      alert("Error in rescoring");
    } finally {
      setLoadingScore(false);
    }
  };

  // 🔥 Skill Gap
  const handleSkillGap = async () => {
    try {
      setLoadingGap(true);
      const response = await getSkillGap(jd);
      setSkillGap(response);
    } catch (err) {
      console.error(err);
      alert("Error in skill gap analysis");
    } finally {
      setLoadingGap(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "900px", margin: "auto" }}>
      <h2>📄 AI Job Description Editor</h2>

      {/* 🔹 Score */}
      <p>
        <strong>ATS Score:</strong>{" "}
        <span style={{ color: getScoreColor(score?.ats_score || 0) }}>
          {score?.ats_score ?? "N/A"}
        </span>
      </p>

      {/* 🔹 Feedback */}
      {score?.feedback?.length > 0 && (
        <div
          style={{
            background: "#fff3cd",
            padding: "10px",
            borderRadius: "6px",
          }}
        >
          <h4>⚠️ Suggestions</h4>
          <ul>
            {score.feedback.map((f: string, i: number) => (
              <li key={i}>{f}</li>
            ))}
          </ul>
        </div>
      )}

      {/* 🔹 Summary */}
      <h3>📌 Summary</h3>
      <textarea
        value={jd.summary || ""}
        onChange={(e) => updateField("summary", e.target.value)}
        style={{ width: "100%", height: "80px" }}
      />

      {/* 🔹 Responsibilities */}
      <h3>📋 Responsibilities</h3>
      {(jd.responsibilities || []).map((item: string, i: number) => (
        <input
          key={i}
          value={item}
          onChange={(e) =>
            updateList("responsibilities", i, e.target.value)
          }
          style={{ width: "100%", marginBottom: "6px" }}
        />
      ))}

      {/* 🔹 Requirements */}
      <h3>✅ Requirements</h3>
      {(jd.requirements || []).map((item: string, i: number) => (
        <input
          key={i}
          value={item}
          onChange={(e) =>
            updateList("requirements", i, e.target.value)
          }
          style={{ width: "100%", marginBottom: "6px" }}
        />
      ))}

      {/* 🔹 Nice to Have */}
      <h3>✨ Nice to Have</h3>
      {(jd.nice_to_have || []).map((item: string, i: number) => (
        <input
          key={i}
          value={item}
          onChange={(e) =>
            updateList("nice_to_have", i, e.target.value)
          }
          style={{ width: "100%", marginBottom: "6px" }}
        />
      ))}

      {/* 🔹 Buttons */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={() => navigate("/")}>🔙 Back</button>

        <button
          onClick={handleRescore}
          disabled={loadingScore}
          style={{ marginLeft: "10px" }}
        >
          {loadingScore ? "Re-scoring..." : "🔄 Re-score"}
        </button>

        <button
          onClick={handleSkillGap}
          disabled={loadingGap}
          style={{ marginLeft: "10px" }}
        >
          {loadingGap ? "Analyzing..." : "🧠 Skill Gap"}
        </button>

        <button
          style={{ marginLeft: "10px" }}
          onClick={() => alert("Job Approved 🚀")}
        >
          ✅ Approve & Publish
        </button>
      </div>

      {/* 🔥 Skill Gap Result */}
      {skillGap && (
        <div
          style={{
            marginTop: "20px",
            background: "#e3f2fd",
            padding: "10px",
            borderRadius: "6px",
          }}
        >
          <h4>🧠 Skill Gap Analysis</h4>

          <p><strong>❌ Missing Skills:</strong></p>
          <ul>
            {skillGap.missing_skills?.map((s: string, i: number) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <p><strong>✅ Market Skills:</strong></p>
          <ul>
            {skillGap.market_skills?.map((s: string, i: number) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResultPage;