import { Mail, Lock, Eye, LogIn, HelpCircle, BarChart3 } from "lucide-react";

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center px-4">
      <div className="w-full max-w-xl">
        {/* Logo Section */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mx-auto shadow-md">
            <BarChart3 className="text-white" size={32} />
          </div>

          <h1 className="mt-5 text-4xl font-bold text-slate-900">
            Student Analyzer System
          </h1>

          <p className="text-slate-500 mt-2">
            Precision insights for academic excellence
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
          {/* Tabs */}
          <div className="flex border-b mb-8">
            <button className="flex-1 py-3 text-blue-600 font-semibold border-b-2 border-blue-600">
              Admin
            </button>

            <button className="flex-1 py-3 text-slate-500 hover:text-slate-700">
              Teacher
            </button>

            <button className="flex-1 py-3 text-slate-500 hover:text-slate-700">
              Student
            </button>
          </div>

          {/* Email */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2 text-slate-700">
              Academic Email
            </label>

            <div className="flex items-center border rounded-lg px-4 py-3">
              <Mail className="text-slate-400 mr-3" size={20} />
              <input
                type="email"
                placeholder="name@university.edu"
                className="w-full outline-none"
              />
            </div>
          </div>

          {/* Password */}
          <div className="mb-6">
            <div className="flex justify-between mb-2">
              <label className="text-sm font-medium text-slate-700">
                Security Password
              </label>

              <a
                href="#"
                className="text-blue-600 text-sm hover:underline"
              >
                Forgot password?
              </a>
            </div>

            <div className="flex items-center border rounded-lg px-4 py-3">
              <Lock className="text-slate-400 mr-3" size={20} />

              <input
                type="password"
                placeholder="••••••••"
                className="w-full outline-none"
              />

              <Eye className="text-slate-400 cursor-pointer" size={20} />
            </div>
          </div>

          {/* Remember */}
          <div className="flex items-center mb-8">
            <input
              type="checkbox"
              className="w-4 h-4 mr-2"
            />
            <span className="text-slate-600">
              Remember me for 30 days
            </span>
          </div>

          {/* Button */}
          <button className="w-full bg-blue-600 hover:bg-blue-700 transition text-white font-semibold py-4 rounded-lg flex items-center justify-center gap-2">
            Login to Dashboard
            <LogIn size={20} />
          </button>

          {/* Help Section */}
          <div className="border-t mt-10 pt-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                <HelpCircle size={20} />
              </div>

              <div>
                <h3 className="font-semibold text-slate-800">
                  Need assistance?
                </h3>

                <p className="text-sm text-slate-500">
                  Contact the university IT helpdesk at
                  help@academic-analyzer.edu
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Status Dot */}
        <div className="mt-6 flex justify-start">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
      </div>
    </div>
  );
}