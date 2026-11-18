import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  MessageSquare,
  FileText,
  Sparkles,
  ArrowRight,
  Shield,
  Cpu,
  Database,
} from "lucide-react";
import GhostFibers from "../components/backgrounds/GhostFibers";

export default function Landing() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Floating physics animation variants for cosmic orb
  const orbFloatVariants = {
    animate: {
      y: [-10, 10, -10],
      rotate: [0, 5, -5, 0],
      transition: {
        duration: 8,
        repeat: Infinity,
        ease: "easeInOut",
      },
    },
  };

  const ringRotateVariants = {
    animate: {
      rotate: 360,
      transition: {
        duration: 25,
        repeat: Infinity,
        ease: "linear",
      },
    },
  };

  const ringReverseVariants = {
    animate: {
      rotate: -360,
      transition: {
        duration: 35,
        repeat: Infinity,
        ease: "linear",
      },
    },
  };

  return (
    <div className="relative min-h-screen bg-[#030712] text-white overflow-x-hidden selection:bg-purple-500/30 selection:text-white">
      {/* ====================================================================
          TOP NAVIGATION BAR
          ==================================================================== */}
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 px-6 sm:px-12 py-4 flex items-center justify-between ${
          scrolled
            ? "bg-[#030712]/80 backdrop-blur-xl border-b border-white/10 shadow-lg shadow-black/40"
            : "bg-transparent"
        }`}
      >
        {/* Brand Logo: Zentora AI */}
        <Link to="/" className="flex items-center gap-2 group">
          <span className="font-serif italic text-2xl md:text-3xl font-bold tracking-tight text-white group-hover:text-purple-300 transition-colors">
            Zentora AI
          </span>
          <span className="text-[10px] font-mono tracking-widest uppercase text-slate-500 border border-white/10 px-2 py-0.5 rounded-full ml-1 hidden sm:inline-block">
            Powered by ROOP
          </span>
        </Link>

        {/* Center Navigation Links */}
        <nav className="hidden md:flex items-center gap-8 text-sm text-slate-300">
          <a
            href="#features"
            className="hover:text-white transition-colors duration-200"
          >
            Features
          </a>
          <a
            href="#workspace"
            className="hover:text-white transition-colors duration-200"
          >
            Workspace
          </a>
          <a
            href="#about"
            className="hover:text-white transition-colors duration-200"
          >
            About
          </a>
        </nav>

        {/* Auth CTA Actions */}
        <div className="flex items-center gap-5">
          <Link
            to="/login"
            className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
          >
            Sign In
          </Link>
          <Link
            to="/signup"
            className="px-5 py-2 rounded-full bg-white text-slate-950 text-sm font-semibold hover:bg-slate-100 transition shadow-md hover:shadow-white/20 active:scale-95"
          >
            Sign Up
          </Link>
        </div>
      </header>

      {/* ====================================================================
          HERO SECTION WITH GHOSTFIBERS BACKGROUND & COSMIC ORB
          ==================================================================== */}
      <section className="relative min-h-screen flex flex-col justify-center items-center pt-28 pb-16 px-4">
        {/* WebGL2 GhostFibers Background */}
        <div className="absolute inset-0 z-0 overflow-hidden pointer-events-auto">
          <GhostFibers
            glowColor="#8b5cf6"
            layers={3}
            twist={1.2}
            threads={72}
            fiberStyle="dots"
            depthOfField={0.85}
            hoverEffect="focus"
            intro
            mouseInteraction
            lineColor="#dfd1fc"
            secondaryColor="#6f4ac5"
            gradient="depth"
            waves={1}
            volume={0.7}
            spread={1}
            scale={1}
            rotation={18}
            perspective={0.65}
            density={1}
            thickness={1}
            tips={0}
            foldGlow={1}
            speed={0.5}
            flow={0.4}
            rollSpeed={0.15}
            focusDepth={0}
            particles={0.5}
            sparkle={0.5}
            glow={0.8}
            brightness={1}
            vignette={0.3}
            grain={0.06}
            mouseStrength={1}
            pulseOnClick
            lightMode={false}
          />
        </div>

        {/* Ambient atmospheric gradients */}
        <div className="absolute inset-0 z-0 bg-radial from-transparent via-[#030712]/60 to-[#030712] pointer-events-none" />

        {/* Hero Content */}
        <div className="relative z-10 max-w-4xl mx-auto text-center flex flex-col items-center">
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-md text-[11px] font-mono tracking-widest text-slate-300 uppercase mb-8 shadow-inner"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
            INTELLIGENT AI WORKSPACE · POWERED BY ROOP
          </motion.div>

          {/* Futuristic 3D Cosmic Orb & Ring Graphic with Z Monogram */}
          <motion.div
            variants={orbFloatVariants}
            animate="animate"
            className="relative w-44 h-44 mb-8 flex items-center justify-center pointer-events-none"
          >
            {/* Outer Cyan Ring */}
            <motion.div
              variants={ringRotateVariants}
              animate="animate"
              className="absolute inset-0 rounded-full border border-cyan-400/30 border-dashed"
            />
            {/* Inner Purple Ring */}
            <motion.div
              variants={ringReverseVariants}
              animate="animate"
              className="absolute inset-3 rounded-full border border-purple-500/40"
              style={{ transform: "rotateX(65deg) rotateY(15deg)" }}
            />
            {/* Glowing Orb Center with Z monogram */}
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-cyan-400 via-indigo-500 to-fuchsia-600 shadow-[0_0_60px_rgba(168,85,247,0.6)] flex items-center justify-center">
              <span className="font-serif italic font-bold text-3xl text-white drop-shadow-md">
                Z
              </span>
            </div>
            {/* Orbiting particles */}
            <div className="absolute top-1 left-4 w-2 h-2 rounded-full bg-cyan-300 shadow-[0_0_8px_#38bdf8] animate-ping" />
            <div className="absolute bottom-2 right-6 w-2.5 h-2.5 rounded-full bg-fuchsia-400 shadow-[0_0_10px_#e879f9]" />
          </motion.div>

          {/* Massive Title: Zentora AI */}
          <motion.h1
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="font-serif italic text-6xl sm:text-7xl md:text-8xl font-bold tracking-tight text-white mb-3"
          >
            Zentora AI
          </motion.h1>

          {/* Subheading: Your Intelligent AI Workspace */}
          <motion.h2
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.3 }}
            className="text-2xl sm:text-3xl md:text-4xl font-semibold text-white tracking-tight mb-2"
          >
            Your Intelligent AI Workspace
          </motion.h2>

          {/* Tagline */}
          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.4 }}
            className="text-base sm:text-lg text-slate-400 font-medium mb-3"
          >
            Ask. Analyze. Create.
          </motion.p>

          {/* Description */}
          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="text-sm sm:text-base text-slate-400 max-w-xl mx-auto mb-8 leading-relaxed"
          >
            A focused workspace for conversations, documents, ideas and intelligent assistance.
          </motion.p>

          {/* Get Started Button */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.6 }}
          >
            <Link
              to="/signup"
              className="group inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full bg-white/5 hover:bg-white/10 border border-white/20 hover:border-white/40 text-white font-medium text-sm transition-all duration-300 backdrop-blur-md shadow-lg hover:shadow-cyan-500/10 active:scale-95"
            >
              <span>Get Started</span>
              <ArrowRight
                size={16}
                className="group-hover:translate-x-1 transition-transform"
              />
            </Link>
          </motion.div>
        </div>

        {/* Feature Preview Cards */}
        <div
          id="features"
          className="relative z-10 w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 mt-20 px-4"
        >
          {/* Card 1: AI Chat */}
          <motion.div
            whileHover={{ y: -4, borderColor: "rgba(168, 85, 247, 0.4)" }}
            transition={{ duration: 0.2 }}
            className="rounded-2xl bg-[#090d1a]/70 border border-white/10 p-6 backdrop-blur-xl shadow-xl flex flex-col"
          >
            <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-cyan-400 mb-4">
              <MessageSquare size={20} />
            </div>
            <h3 className="text-base font-semibold text-white mb-2">AI Chat</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Ask questions, solve problems and have thoughtful conversations through natural AI dialog.
            </p>
          </motion.div>

          {/* Card 2: Document Assistant */}
          <motion.div
            whileHover={{ y: -4, borderColor: "rgba(56, 189, 248, 0.4)" }}
            transition={{ duration: 0.2 }}
            className="rounded-2xl bg-[#090d1a]/70 border border-white/10 p-6 backdrop-blur-xl shadow-xl flex flex-col"
          >
            <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-purple-400 mb-4">
              <FileText size={20} />
            </div>
            <h3 className="text-base font-semibold text-white mb-2">
              Document Assistant
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Upload documents and ask questions using intelligent RAG retrieval without reading every page.
            </p>
          </motion.div>

          {/* Card 3: Smart Workspace */}
          <motion.div
            whileHover={{ y: -4, borderColor: "rgba(236, 72, 153, 0.4)" }}
            transition={{ duration: 0.2 }}
            className="rounded-2xl bg-[#090d1a]/70 border border-white/10 p-6 backdrop-blur-xl shadow-xl flex flex-col"
          >
            <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-fuchsia-400 mb-4">
              <Sparkles size={20} />
            </div>
            <h3 className="text-base font-semibold text-white mb-2">
              Smart Workspace
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              One focused workspace for thinking, writing, code generation, and intelligent productivity.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer
        id="about"
        className="relative z-10 border-t border-white/10 py-8 px-6 text-center text-xs text-slate-500"
      >
        <p>© {new Date().getFullYear()} Zentora AI. Your workspace. Your intelligence. · Powered by ROOP</p>
      </footer>
    </div>
  );
}
