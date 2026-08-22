"use client";

import { useEffect, useRef, useState } from "react";

interface ObjectAnalysis {
  name: string;
  description: string;
}

interface Analysis {
  caption: string;
  description: string;
  scene: string;
  objects: ObjectAnalysis[];
  activities: string[];
}

interface AnalysisResponse {
  success: boolean;
  filename: string;
  analysis: Analysis;
}

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Reference to the file input
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Clean up preview URL when component is removed
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    // Allowed file types
    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Please select a JPG, PNG, or WEBP image.");
      return;
    }

    // Maximum file size = 10 MB
    const maxSize = 10 * 1024 * 1024;

    if (file.size > maxSize) {
      setError("Image size must be less than 10 MB.");
      return;
    }

    // Remove previous preview URL
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    const url = URL.createObjectURL(file);

    setSelectedFile(file);
    setPreviewUrl(url);

    // Clear previous result/error
    setResult(null);
    setError(null);
  };


  const analyzeImage = async () => {
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();

      formData.append("image", selectedFile);

      const response = await fetch(
        "http://127.0.0.1:8000/api/analyze-image",
        {
          method: "POST",
          body: formData,
        }
      );

      // Show actual backend error
      if (!response.ok) {
        const errorText = await response.text();

        console.error("Backend error:", errorText);

        throw new Error(
          `Server error ${response.status}: ${errorText}`
        );
      }

      const data: AnalysisResponse = await response.json();

      setResult(data);
    } catch (err) {
      console.error("Analysis failed:", err);

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError(
          "Something went wrong while analyzing the image."
        );
      }
    } finally {
      setLoading(false);
    }
  };


  const analyzeAnotherImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setLoading(false);

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    // Scroll back to upload section
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <main className="min-h-screen bg-slate-950 text-white px-6 py-12">
      <div className="mx-auto max-w-5xl">

        <section className="text-center mb-12">

          <div className="inline-flex items-center rounded-full border border-slate-700 bg-slate-900 px-4 py-2 text-sm text-slate-300 mb-5">
             Gemini Vision Powered
          </div>

          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            VisionAI
          </h1>

          <p className="mt-5 text-lg text-slate-400 max-w-2xl mx-auto">
            Upload an image and let AI understand the scene,
            identify objects, and generate a meaningful description.
          </p>

        </section>

        <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 md:p-10">

          <div className="text-center">

            <h2 className="text-2xl font-semibold mb-2">
              Analyze an Image
            </h2>

            <p className="text-slate-400 mb-8">
              Choose a JPG, PNG, or WEBP image.
              Maximum size: 10 MB.
            </p>


            {/* IMAGE UPLOAD AREA */}
            <label
              htmlFor="image-upload"
              className="mx-auto flex min-h-72 max-w-3xl cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-700 bg-slate-950/50 px-6 transition hover:border-blue-500 hover:bg-slate-950"
            >

              {!previewUrl ? (
                <>
                  <div className="text-6xl mb-5">
    
                  </div>

                  <p className="text-lg font-medium">
                    Upload your image
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    Click here to browse your computer
                  </p>
                </>
              ) : (
                <img
                  src={previewUrl}
                  alt="Selected image preview"
                  className="max-h-80 max-w-full rounded-xl object-contain"
                />
              )}

              <input
                ref={fileInputRef}
                id="image-upload"
                type="file"
                accept="image/jpeg,image/png,image/webp"
                onChange={handleFileChange}
                className="hidden"
              />

            </label>


            {/* SELECTED FILE */}
            {selectedFile && (
              <div className="mt-5 text-sm text-slate-400">

                Selected:{" "}

                <span className="text-white font-medium">
                  {selectedFile.name}
                </span>

                <span className="ml-2 text-slate-500">
                  ({(selectedFile.size / (1024 * 1024)).toFixed(2)} MB)
                </span>

              </div>
            )}


            {/* ANALYZE BUTTON */}
            {selectedFile && !result && (
              <button
                onClick={analyzeImage}
                disabled={loading}
                className="mt-6 rounded-xl bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >

                {loading ? (
                  <span className="flex items-center gap-2">
                    <span className="animate-spin">
                      ⏳
                    </span>

                    Analyzing with Gemini...
                  </span>
                ) : (
                  " Analyze Image"
                )}

              </button>
            )}


            {/* ERROR */}
            {error && (
              <div className="mx-auto mt-5 max-w-2xl rounded-xl border border-red-900/50 bg-red-950/30 px-5 py-4">

                <p className="text-sm text-red-400">
                  {error}
                </p>

              </div>
            )}

          </div>

        </section>

        {result && (
          <section className="mt-10 space-y-6">

            {/* RESULTS HEADER */}
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">

                <div>
                  <p className="text-sm text-slate-500">
                    Analysis completed for
                  </p>

                  <h2 className="mt-1 text-xl font-semibold">
                    {result.filename}
                  </h2>
                </div>

                <div className="rounded-full bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
                  ✓ Analysis Complete
                </div>

              </div>

            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <h2 className="mb-4 text-2xl font-semibold">
                 AI Caption
              </h2>

              <p className="text-lg leading-8 text-slate-300">
                {result.analysis.caption}
              </p>

            </div>


    
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <h2 className="mb-4 text-2xl font-semibold">
                📖 Detailed Description
              </h2>

              <p className="leading-8 text-slate-300">
                {result.analysis.description}
              </p>

            </div>


            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <h2 className="mb-4 text-2xl font-semibold">
                 Scene
              </h2>

              <p className="text-slate-300">
                {result.analysis.scene}
              </p>

            </div>


            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <div className="flex items-center justify-between mb-6">

                <h2 className="text-2xl font-semibold">
                  🔍 Detected Objects
                </h2>

                <span className="rounded-full bg-blue-500/10 px-3 py-1 text-sm text-blue-400">
                  {result.analysis.objects.length} detected
                </span>

              </div>


              {result.analysis.objects.length > 0 ? (
                <div className="grid gap-4 md:grid-cols-2">

                  {result.analysis.objects.map(
                    (object, index) => (

                      <div
                        key={index}
                        className="rounded-2xl border border-slate-700 bg-slate-950 p-5 transition hover:border-slate-600"
                      >

                        <div className="flex items-start gap-3">

                          <div className="text-2xl">
                            🔹
                          </div>

                          <div>

                            <h3 className="font-semibold text-white">
                              {object.name}
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                              {object.description}
                            </p>

                          </div>

                        </div>

                      </div>

                    )
                  )}

                </div>
              ) : (
                <p className="text-slate-400">
                  No major objects detected.
                </p>
              )}

            </div>
            <div className="rounded-3xl border border-slate-800 bg-slate-900 p-6 md:p-8">

              <h2 className="mb-4 text-2xl font-semibold">
                🚶 Activities
              </h2>

              {result.analysis.activities.length > 0 ? (

                <ul className="space-y-2 text-slate-300">

                  {result.analysis.activities.map(
                    (activity, index) => (

                      <li key={index}>
                        • {activity}
                      </li>

                    )
                  )}

                </ul>

              ) : (

                <p className="text-slate-400">
                  No visible activities detected.
                </p>

              )}

            </div>

            <div className="flex justify-center py-6">

              <button
                onClick={analyzeAnotherImage}
                className="rounded-xl border border-slate-700 bg-slate-900 px-8 py-3 font-semibold text-white transition hover:border-blue-500 hover:bg-slate-800"
              >
                Analyze Another Image
              </button>

            </div>

          </section>
        )}

      </div>
    </main>
  );
}