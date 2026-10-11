import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CreateJob from "./pages/CreateJob";
import ResultPage from "./pages/ResultPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CreateJob />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </Router>
  );
}

export default App;