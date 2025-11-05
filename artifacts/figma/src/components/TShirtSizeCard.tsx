import { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

export function TShirtSizeCard() {
  const [height, setHeight] = useState('175');
  const [weight, setWeight] = useState('70');
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [fitPreference, setFitPreference] = useState<'slim' | 'regular' | 'loose'>('regular');
  const [recommendedSize, setRecommendedSize] = useState<string | null>(null);

  const calculateSize = () => {
    const h = parseInt(height);
    const w = parseInt(weight);
    
    // Simple T-shirt size recommendation logic
    const bmi = w / Math.pow(h / 100, 2);
    
    let size = 'M';
    
    if (gender === 'male') {
      if (bmi < 18.5) {
        size = fitPreference === 'slim' ? 'XS' : 'S';
      } else if (bmi < 25) {
        size = fitPreference === 'slim' ? 'S' : fitPreference === 'loose' ? 'L' : 'M';
      } else if (bmi < 30) {
        size = fitPreference === 'slim' ? 'M' : fitPreference === 'loose' ? 'XL' : 'L';
      } else {
        size = fitPreference === 'slim' ? 'L' : 'XL';
      }
    } else {
      if (bmi < 18.5) {
        size = fitPreference === 'slim' ? 'XS' : 'S';
      } else if (bmi < 25) {
        size = fitPreference === 'slim' ? 'XS' : fitPreference === 'loose' ? 'M' : 'S';
      } else if (bmi < 30) {
        size = fitPreference === 'slim' ? 'S' : fitPreference === 'loose' ? 'L' : 'M';
      } else {
        size = fitPreference === 'slim' ? 'M' : 'L';
      }
    }
    
    setRecommendedSize(size);
  };

  const getEffortDescription = (size: string) => {
    const descriptions: Record<string, string> = {
      'XS': 'Extra Small - Minimal effort',
      'S': 'Small - Light effort',
      'M': 'Medium - Moderate effort',
      'L': 'Large - Significant effort',
      'XL': 'Extra Large - Major effort',
    };
    return descriptions[size] || 'Medium - Moderate effort';
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-blue-500" />
            AI T-Shirt Size Recommendation
          </CardTitle>
          <CardDescription>
            Get personalized T-shirt size recommendations based on your measurements
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Height (cm)</Label>
              <Input
                type="number"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
                placeholder="175"
              />
            </div>
            <div className="space-y-2">
              <Label>Weight (kg)</Label>
              <Input
                type="number"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                placeholder="70"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Gender</Label>
              <Select value={gender} onValueChange={(value: 'male' | 'female') => setGender(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Fit Preference</Label>
              <Select value={fitPreference} onValueChange={(value: 'slim' | 'regular' | 'loose') => setFitPreference(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="slim">Slim</SelectItem>
                  <SelectItem value="regular">Regular</SelectItem>
                  <SelectItem value="loose">Loose</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button onClick={calculateSize} className="w-full">
            <Sparkles className="w-4 h-4 mr-2" />
            Get Recommendation
          </Button>
        </CardContent>
      </Card>

      {recommendedSize && (
        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-32 h-32 bg-white rounded-full border-4 border-blue-500 shadow-lg">
                <span className="text-6xl text-blue-600">{recommendedSize}</span>
              </div>
              <div>
                <h3 className="text-slate-900 mb-2">T-Shirt Size Recommendation:</h3>
                <p className="text-slate-600">{getEffortDescription(recommendedSize)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="bg-slate-50">
        <CardHeader>
          <CardTitle className="text-base">About This Feature</CardTitle>
        </CardHeader>
        <CardContent className="text-sm text-slate-600 space-y-2">
          <p>
            This AI-powered feature demonstrates how Agile TaskIQ can leverage artificial intelligence 
            to provide intelligent recommendations.
          </p>
          <p>
            The T-shirt sizing metaphor is commonly used in agile development to estimate task complexity 
            (XS, S, M, L, XL), making this a perfect showcase of our AI capabilities.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
