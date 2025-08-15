# Contributing to Car Price Predictor

Thank you for your interest in contributing to the Car Price Predictor project! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Git

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/car-price-predictor.git
   cd car-price-predictor
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open http://localhost:3000 in your browser

## 📝 Development Guidelines

### Code Style

- Use TypeScript for all new code
- Follow the existing code style and formatting
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### File Structure

```
src/
├── app/                    # Next.js app directory
│   ├── api/               # API routes
│   ├── batch/             # Batch prediction page
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── batch-prediction.tsx
│   └── car-prediction-form.tsx
├── lib/                  # Utility functions
│   ├── api.ts           # API functions
│   └── utils.ts         # Helper functions
└── types/               # TypeScript type definitions
    └── car.ts
```

### Component Guidelines

- Use functional components with hooks
- Implement proper TypeScript interfaces
- Add proper error handling
- Include loading states
- Make components responsive

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test on different screen sizes
- Test error scenarios

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run docker:build` - Build Docker image
- `npm run docker:run` - Run Docker container
- `npm run docker:compose` - Start with Docker Compose

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to reproduce**: Step-by-step instructions
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: Browser, OS, Node.js version
6. **Screenshots**: If applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Description**: Clear description of the feature
2. **Use case**: Why this feature is needed
3. **Proposed solution**: How you think it should work
4. **Alternatives**: Any alternative solutions considered

## 🔄 Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, well-documented code
   - Add tests if applicable
   - Update documentation

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Use a descriptive title
   - Include a detailed description
   - Reference any related issues
   - Add screenshots if UI changes

### Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(form): add validation for car specifications
fix(api): handle API connection errors
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Writing Tests

- Test component behavior, not implementation
- Use meaningful test descriptions
- Test both success and error scenarios
- Mock external dependencies

## 📚 Documentation

### Code Documentation

- Add JSDoc comments for functions
- Document complex algorithms
- Include examples for API functions
- Update README for new features

### User Documentation

- Update user guides for new features
- Add screenshots for UI changes
- Include troubleshooting steps
- Keep deployment guides current

## 🎨 UI/UX Guidelines

### Design Principles

- Keep it simple and intuitive
- Ensure accessibility (WCAG 2.1 AA)
- Use consistent spacing and typography
- Provide clear feedback for user actions

### Responsive Design

- Mobile-first approach
- Test on various screen sizes
- Ensure touch targets are adequate
- Optimize for performance

### Accessibility

- Use semantic HTML
- Include proper ARIA labels
- Ensure keyboard navigation
- Test with screen readers

## 🔒 Security

### Security Guidelines

- Never commit sensitive data
- Validate all user inputs
- Use HTTPS in production
- Follow OWASP guidelines
- Keep dependencies updated

### Security Reporting

If you discover a security vulnerability:

1. **DO NOT** create a public issue
2. Email the maintainers directly
3. Include detailed information
4. Allow time for response

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn
- Provide constructive feedback
- Follow the project's code of conduct

### Communication

- Use clear, professional language
- Be patient with newcomers
- Ask questions when unsure
- Share knowledge and resources

## 📋 Review Process

### Pull Request Review

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** updates
5. **Final approval** and merge

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security issues introduced
- [ ] Performance impact considered
- [ ] Accessibility maintained

## 🏆 Recognition

Contributors will be recognized in:

- Project README
- Release notes
- Contributor hall of fame
- GitHub contributors page

## 📞 Getting Help

### Questions and Support

- Check existing issues and discussions
- Search documentation
- Ask in discussions
- Contact maintainers

### Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🎯 Contribution Ideas

### Good First Issues

- Documentation improvements
- Bug fixes
- UI/UX enhancements
- Performance optimizations
- Accessibility improvements

### Advanced Contributions

- New features
- API improvements
- Testing infrastructure
- Deployment automation
- Performance monitoring

---

Thank you for contributing to Car Price Predictor! 🚗💰
