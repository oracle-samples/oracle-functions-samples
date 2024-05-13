FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add ListCompartment.csproj
RUN dotnet build ListCompartment.csproj -c Release
RUN dotnet publish ListCompartment.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "ListCompartment.dll"]
CMD ["ListCompartment:Function:function_handler"]